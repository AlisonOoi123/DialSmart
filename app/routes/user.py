"""
User Routes
Main user-facing pages and functionality
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Brand, Phone, PhoneSpecification, UserPreference, Recommendation, Comparison, ContactMessage
from app.modules import AIRecommendationEngine
from app.utils.helpers import parse_json_field, validate_password
import json
from datetime import datetime

bp = Blueprint('user', __name__)

@bp.route('/')
def index():
    """Landing page"""
    # Get featured brands
    featured_brands = Brand.query.filter_by(is_featured=True, is_active=True).limit(10).all()

    # Get latest phones
    latest_phones = Phone.query.filter_by(is_active=True)\
        .order_by(Phone.created_at.desc())\
        .limit(6)\
        .all()

    return render_template('user/index.html',
                         featured_brands=featured_brands,
                         latest_phones=latest_phones)

@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    # Get user's recent recommendations
    recent_recommendations = Recommendation.query.filter_by(user_id=current_user.id)\
        .order_by(Recommendation.created_at.desc())\
        .limit(5)\
        .all()

    # Get saved comparisons
    saved_comparisons = Comparison.query.filter_by(user_id=current_user.id, is_saved=True)\
        .order_by(Comparison.created_at.desc())\
        .limit(5)\
        .all()

    # Get user preferences
    preferences = UserPreference.query.filter_by(user_id=current_user.id).first()

    return render_template('user/dashboard.html',
                         recommendations=recent_recommendations,
                         comparisons=saved_comparisons,
                         preferences=preferences)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name', current_user.full_name)
        current_user.user_category = request.form.get('user_category', current_user.user_category)
        current_user.age_range = request.form.get('age_range', current_user.age_range)

        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            current_password = request.form.get('current_password')
            if current_user.check_password(current_password):
                # Validate new password strength
                is_valid, error_message = validate_password(new_password)
                if not is_valid:
                    flash(error_message, 'danger')
                    return render_template('user/profile.html')

                current_user.set_password(new_password)
                flash('Password updated successfully.', 'success')
            else:
                flash('Current password is incorrect.', 'danger')
                return render_template('user/profile.html')

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user.profile'))

    return render_template('user/profile.html')

@bp.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    """User preference settings"""
    user_prefs = UserPreference.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        if not user_prefs:
            user_prefs = UserPreference(user_id=current_user.id)
            db.session.add(user_prefs)

        # Update preferences from form
        user_prefs.min_budget = int(request.form.get('min_budget', 500))
        user_prefs.max_budget = int(request.form.get('max_budget', 5000))
        user_prefs.min_ram = int(request.form.get('min_ram', 4))
        user_prefs.min_storage = int(request.form.get('min_storage', 64))
        user_prefs.min_camera = int(request.form.get('min_camera', 12))
        user_prefs.min_battery = int(request.form.get('min_battery', 3000))
        user_prefs.requires_5g = bool(request.form.get('requires_5g'))
        user_prefs.min_screen_size = float(request.form.get('min_screen_size', 5.5))
        user_prefs.max_screen_size = float(request.form.get('max_screen_size', 7.0))

        # Store JSON fields
        primary_usage = request.form.getlist('primary_usage')
        user_prefs.primary_usage = json.dumps(primary_usage)

        important_features = request.form.getlist('important_features')
        user_prefs.important_features = json.dumps(important_features)

        preferred_brands = request.form.getlist('preferred_brands')
        user_prefs.preferred_brands = json.dumps(preferred_brands)

        db.session.commit()
        flash('Preferences updated successfully.', 'success')
        return redirect(url_for('user.dashboard'))

    # Get all brands for preference selection
    all_brands = Brand.query.filter_by(is_active=True).all()

    return render_template('user/preferences.html',
                         preferences=user_prefs,
                         brands=all_brands)

@bp.route('/recommendations')
@login_required
def recommendations():
    """Show AI recommendations for current user"""
    ai_engine = AIRecommendationEngine()

    # Get recommendations
    recommendations = ai_engine.get_recommendations(current_user.id, top_n=5)

    return render_template('user/recommendations.html',
                         recommendations=recommendations)

@bp.route('/recommendations/history')
@login_required
def recommendation_history():
    """View recommendation history"""
    history = Recommendation.query.filter_by(user_id=current_user.id)\
        .order_by(Recommendation.created_at.desc())\
        .all()

    return render_template('user/recommendation_history.html',
                         history=history)

@bp.route('/recommendation/wizard', methods=['GET', 'POST'])
def recommendation_wizard():
    """Multi-step recommendation wizard"""
    if request.method == 'POST':
        # Process wizard form
        criteria = {
            'min_budget': int(request.form.get('min_budget', 500)),
            'max_budget': int(request.form.get('max_budget', 5000)),
            'primary_usage': request.form.getlist('primary_usage'),
            'important_features': request.form.getlist('important_features'),
            'preferred_brands': request.form.getlist('preferred_brands'),
            # Add reasonable defaults for specs not collected by wizard
            'min_ram': 4,  # 4GB minimum
            'min_storage': 64,  # 64GB minimum
            'min_camera': 12,  # 12MP minimum
            'min_battery': 3000,  # 3000mAh minimum
            'requires_5g': '5G' in request.form.getlist('important_features'),  # Check if 5G was selected
            'min_screen_size': 5.5,
            'max_screen_size': 7.0
        }

        # Get AI recommendations
        ai_engine = AIRecommendationEngine()
        recommendations = ai_engine.get_recommendations(
            current_user.id if current_user.is_authenticated else None,
            criteria=criteria,
            top_n=5  # Get top 5 instead of 3 for better results
        )

        return render_template('user/wizard_results.html',
                             recommendations=recommendations,
                             criteria=criteria)

    # Get brands for wizard
    brands = Brand.query.filter_by(is_active=True).all()

    return render_template('user/wizard.html', brands=brands)

@bp.route('/browse')
def browse():
    """Browse all phones with filters"""
    # Get filter parameters
    brand_id = request.args.get('brand_id', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    has_5g = request.args.get('has_5g', type=bool)
    sort_by = request.args.get('sort_by', 'created_at')
    page = request.args.get('page', 1, type=int)

    # Build query
    query = Phone.query.filter_by(is_active=True)

    if brand_id:
        query = query.filter_by(brand_id=brand_id)

    if min_price:
        query = query.filter(Phone.price >= min_price)

    if max_price:
        query = query.filter(Phone.price <= max_price)

    # Apply sorting
    if sort_by == 'price_asc':
        query = query.order_by(Phone.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Phone.price.desc())
    elif sort_by == 'name':
        query = query.order_by(Phone.model_name.asc())
    else:  # newest - sort by launch date (release_date)
        query = query.order_by(Phone.release_date.desc().nullslast(), Phone.created_at.desc())

    # Paginate
    per_page = 12
    phones = query.paginate(page=page, per_page=per_page, error_out=False)

    # Get all brands for filter
    brands = Brand.query.filter_by(is_active=True).all()

    return render_template('user/browse.html',
                         phones=phones,
                         brands=brands,
                         current_filters={
                             'brand_id': brand_id,
                             'min_price': min_price,
                             'max_price': max_price,
                             'has_5g': has_5g,
                             'sort_by': sort_by
                         })

@bp.route('/about')
def about():
    """About page"""
    return render_template('user/about.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        # Process contact form
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject', 'General Inquiry')
        message = request.form.get('message')

        # Validate required fields
        if not all([name, email, message]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('user/contact.html')

        # Create and save contact message
        contact_msg = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message,
            is_read=0,  # Oracle uses 0/1 instead of False/True
            is_replied=0,
            created_at=datetime.utcnow()
        )

        try:
            db.session.add(contact_msg)
            db.session.commit()
            flash('Thank you for contacting us. We will get back to you soon.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again later.', 'danger')

        return redirect(url_for('user.contact'))

    return render_template('user/contact.html')
