"""
API Routes
RESTful API endpoints for AJAX requests and chatbot
"""
from flask import Blueprint, jsonify, request, send_file, current_app
from flask_login import login_required, current_user
from app.models import Phone, PhoneSpecification, Brand, Comparison
from app.modules import ChatbotEngine, AIRecommendationEngine, PhoneComparison
from app import db
import uuid
import requests
from io import BytesIO
from datetime import datetime, timedelta
import hashlib

bp = Blueprint('api', __name__, url_prefix='/api')

# Simple in-memory cache for images (could be replaced with Redis in production)
image_cache = {}

# Image proxy endpoint
@bp.route('/image-proxy', methods=['GET'])
def image_proxy():
    """
    Proxy external images to bypass CORS and hotlinking protection
    Usage: /api/image-proxy?url=<encoded_image_url>
    """
    image_url = request.args.get('url')

    if not image_url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        # Generate cache key
        cache_key = hashlib.md5(image_url.encode()).hexdigest()

        # Check cache (valid for 1 hour)
        if cache_key in image_cache:
            cached_data, cached_time, content_type = image_cache[cache_key]
            if datetime.utcnow() - cached_time < timedelta(hours=1):
                return send_file(
                    BytesIO(cached_data),
                    mimetype=content_type,
                    as_attachment=False,
                    download_name='image.webp'
                )

        # Fetch image with proper headers to bypass hotlinking protection
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.mobile57.com/',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site'
        }

        # Fetch image with timeout
        response = requests.get(image_url, headers=headers, timeout=10, stream=True)
        response.raise_for_status()

        # Get content type
        content_type = response.headers.get('Content-Type', 'image/webp')

        # Read image data
        image_data = response.content

        # Cache it (limit cache size to prevent memory issues)
        if len(image_cache) < 100:  # Limit cache to 100 images
            image_cache[cache_key] = (image_data, datetime.utcnow(), content_type)

        # Return image
        return send_file(
            BytesIO(image_data),
            mimetype=content_type,
            as_attachment=False,
            download_name='image.webp'
        )

    except requests.exceptions.Timeout:
        current_app.logger.error(f"Image proxy timeout for URL: {image_url}")
        return jsonify({'error': 'Image request timed out'}), 504
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Image proxy error for URL {image_url}: {str(e)}")
        return jsonify({'error': 'Failed to fetch image'}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in image proxy: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Chatbot endpoints
@bp.route('/chat', methods=['POST'])
def chat():
    """Process chatbot message (available for guests and logged-in users)"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id') or str(uuid.uuid4())

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Get user_id (None for guests)
        user_id = current_user.id if current_user.is_authenticated else None

        # Process with chatbot engine
        chatbot = ChatbotEngine()
        response = chatbot.process_message(user_id, message, session_id)

        return jsonify({
            'success': True,
            'response': response['response'],
            'type': response.get('type', 'text'),
            'metadata': response.get('metadata', {}),
            'quick_replies': response.get('quick_replies', []),
            'session_id': session_id
        })
    except Exception as e:
        current_app.logger.error(f"Chatbot error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'Failed to process message',
            'message': str(e)
        }), 500

@bp.route('/chat/history', methods=['GET'])
@login_required
def chat_history():
    """Get chat history"""
    session_id = request.args.get('session_id')
    limit = request.args.get('limit', 50, type=int)

    chatbot = ChatbotEngine()
    history = chatbot.get_chat_history(current_user.id, session_id, limit)

    chat_list = [{
        'id': chat.id,
        'message': chat.message,
        'response': chat.response,
        'intent': chat.intent,
        'created_at': chat.created_at.isoformat()
    } for chat in history]

    return jsonify({
        'success': True,
        'history': chat_list
    })

# Phone search endpoint
@bp.route('/phones/search', methods=['GET'])
def search_phones():
    """Search phones (for autocomplete)"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)

    if not query:
        return jsonify({'phones': []})

    phones = Phone.query.filter(
        Phone.is_active == True,
        Phone.model_name.ilike(f'%{query}%')
    ).limit(limit).all()

    phone_list = [{
        'id': phone.id,
        'name': phone.model_name,
        'brand': phone.brand.name if phone.brand else 'Unknown',
        'price': phone.price,
        'image': phone.main_image
    } for phone in phones]

    return jsonify({
        'success': True,
        'phones': phone_list
    })

# Phone details endpoint
@bp.route('/phones/<int:phone_id>', methods=['GET'])
def get_phone_details(phone_id):
    """Get phone details"""
    phone = Phone.query.get_or_404(phone_id)
    specs = PhoneSpecification.query.filter_by(phone_id=phone_id).first()

    phone_data = {
        'id': phone.id,
        'model_name': phone.model_name,
        'brand': phone.brand.name if phone.brand else 'Unknown',
        'price': phone.price,
        'main_image': phone.main_image,
        'availability_status': phone.availability_status
    }

    if specs:
        phone_data['specs'] = {
            'screen_size': specs.screen_size,
            'screen_resolution': specs.screen_resolution,
            'screen_type': specs.screen_type,
            'processor': specs.processor,
            'ram_options': specs.ram_options,
            'storage_options': specs.storage_options,
            'rear_camera': specs.rear_camera,
            'front_camera': specs.front_camera,
            'battery_capacity': specs.battery_capacity,
            'has_5g': specs.has_5g,
            'operating_system': specs.operating_system
        }

    return jsonify({
        'success': True,
        'phone': phone_data
    })

# Recommendation endpoint
@bp.route('/recommendations', methods=['POST'])
@login_required
def get_recommendations():
    """Get AI recommendations"""
    data = request.get_json()
    criteria = data.get('criteria', {})
    top_n = data.get('top_n', 3)

    ai_engine = AIRecommendationEngine()
    recommendations = ai_engine.get_recommendations(
        current_user.id,
        criteria=criteria if criteria else None,
        top_n=top_n
    )

    rec_list = []
    for rec in recommendations:
        phone = rec['phone']
        specs = rec['specifications']

        rec_data = {
            'phone_id': phone.id,
            'model_name': phone.model_name,
            'brand': phone.brand.name if phone.brand else 'Unknown',
            'price': phone.price,
            'match_score': rec['match_score'],
            'reasoning': rec['reasoning'],
            'main_image': phone.main_image
        }

        if specs:
            rec_data['key_specs'] = {
                'ram': specs.ram_options,
                'storage': specs.storage_options,
                'camera': f"{specs.rear_camera_main}MP" if specs.rear_camera_main else 'N/A',
                'battery': f"{specs.battery_capacity}mAh" if specs.battery_capacity else 'N/A'
            }

        rec_list.append(rec_data)

    return jsonify({
        'success': True,
        'recommendations': rec_list
    })

# Brands endpoint
@bp.route('/brands', methods=['GET'])
def get_brands():
    """Get all active brands"""
    brands = Brand.query.filter_by(is_active=True).order_by(Brand.name).all()

    brand_list = [{
        'id': brand.id,
        'name': brand.name,
        'logo_url': brand.logo_url,
        'phone_count': brand.get_phone_count()
    } for brand in brands]

    return jsonify({
        'success': True,
        'brands': brand_list
    })

# Phone filter endpoint
@bp.route('/phones/filter', methods=['POST'])
def filter_phones():
    """Filter phones based on criteria"""
    data = request.get_json()

    brand_ids = data.get('brand_ids', [])
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    min_ram = data.get('min_ram')
    has_5g = data.get('has_5g')
    min_battery = data.get('min_battery')
    page = data.get('page', 1)
    per_page = data.get('per_page', 12)

    # Build query
    query = Phone.query.filter_by(is_active=True)

    if brand_ids:
        query = query.filter(Phone.brand_id.in_(brand_ids))

    if min_price:
        query = query.filter(Phone.price >= min_price)

    if max_price:
        query = query.filter(Phone.price <= max_price)

    # Join with specifications for advanced filters
    if min_ram or has_5g or min_battery:
        query = query.join(PhoneSpecification)

        if min_ram:
            # This is simplified - in production, parse ram_options properly
            query = query.filter(PhoneSpecification.ram_options.ilike(f'%{min_ram}GB%'))

        if has_5g:
            query = query.filter(PhoneSpecification.has_5g == True)

        if min_battery:
            query = query.filter(PhoneSpecification.battery_capacity >= min_battery)

    # Paginate
    phones = query.paginate(page=page, per_page=per_page, error_out=False)

    phone_list = [{
        'id': phone.id,
        'model_name': phone.model_name,
        'brand': phone.brand.name if phone.brand else 'Unknown',
        'price': phone.price,
        'main_image': phone.main_image
    } for phone in phones.items]

    return jsonify({
        'success': True,
        'phones': phone_list,
        'total': phones.total,
        'pages': phones.pages,
        'current_page': phones.page
    })

# Quick stats endpoint
@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get quick statistics"""
    total_phones = Phone.query.filter_by(is_active=True).count()
    total_brands = Brand.query.filter_by(is_active=True).count()

    # Get price range
    phones = Phone.query.filter_by(is_active=True).all()
    prices = [phone.price for phone in phones]

    return jsonify({
        'success': True,
        'stats': {
            'total_phones': total_phones,
            'total_brands': total_brands,
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0
        }
    })

# Comparison save endpoint
@bp.route('/comparison/save', methods=['POST'])
@login_required
def save_comparison():
    """Save a comparison"""
    try:
        data = request.get_json()
        phone1_id = data.get('phone1_id')
        phone2_id = data.get('phone2_id')

        if not phone1_id or not phone2_id:
            return jsonify({
                'success': False,
                'error': 'Both phone IDs are required'
            }), 400

        # Check if comparison already exists
        existing_comparison = Comparison.query.filter_by(
            user_id=current_user.id,
            phone1_id=phone1_id,
            phone2_id=phone2_id
        ).first()

        if existing_comparison:
            # Update existing comparison to saved
            existing_comparison.is_saved = True
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Comparison updated successfully'
            })

        # Create new saved comparison
        comparison = Comparison(
            user_id=current_user.id,
            phone1_id=phone1_id,
            phone2_id=phone2_id,
            is_saved=True
        )
        db.session.add(comparison)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Comparison saved successfully'
        })

    except Exception as e:
        current_app.logger.error(f"Error saving comparison: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
