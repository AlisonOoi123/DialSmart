"""
API Routes
RESTful API endpoints for AJAX requests and chatbot
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Phone, PhoneSpecification, Brand
from app.modules import ChatbotEngine, AIRecommendationEngine
import uuid

bp = Blueprint('api', __name__, url_prefix='/api')

# Chatbot endpoints
@bp.route('/chat', methods=['POST'])
@login_required
def chat():
    """Process chatbot message"""
    data = request.get_json()
    message = data.get('message', '')
    session_id = data.get('session_id') or str(uuid.uuid4())

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    # Process with chatbot engine
    chatbot = ChatbotEngine()
    response = chatbot.process_message(current_user.id, message, session_id)

    return jsonify({
        'success': True,
        'response': response['response'],
        'type': response.get('type', 'text'),
        'metadata': response.get('metadata', {}),
        'quick_replies': response.get('quick_replies', []),
        'session_id': session_id
    })

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
