"""
Phone Routes
Phone details, brand pages, and comparison functionality
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Phone, PhoneSpecification, Brand
from app.modules import PhoneComparison, AIRecommendationEngine

bp = Blueprint('phone', __name__, url_prefix='/phone')

@bp.route('/<int:phone_id>')
def details(phone_id):
    """Phone details page"""
    phone = Phone.query.get_or_404(phone_id)
    specs = PhoneSpecification.query.filter_by(phone_id=phone_id).first()

    # Get similar phones
    ai_engine = AIRecommendationEngine()
    similar_phones = ai_engine.get_similar_phones(phone_id, top_n=3)

    return render_template('phone/details.html',
                         phone=phone,
                         specs=specs,
                         similar_phones=similar_phones)

@bp.route('/brand/<int:brand_id>')
def brand_page(brand_id):
    """Brand page showing all phones from a brand"""
    brand = Brand.query.get_or_404(brand_id)

    # Get filter parameters
    sort_by = request.args.get('sort_by', 'created_at')
    page = request.args.get('page', 1, type=int)

    # Build query
    query = Phone.query.filter_by(brand_id=brand_id, is_active=True)

    # Apply sorting
    if sort_by == 'price_asc':
        query = query.order_by(Phone.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Phone.price.desc())
    elif sort_by == 'name':
        query = query.order_by(Phone.model_name.asc())
    else:  # created_at
        query = query.order_by(Phone.created_at.desc())

    # Paginate
    per_page = 12
    phones = query.paginate(page=page, per_page=per_page, error_out=False)

    # Get brand statistics
    phone_count = brand.get_phone_count()
    price_range = brand.get_price_range()

    return render_template('phone/brand.html',
                         brand=brand,
                         phones=phones,
                         phone_count=phone_count,
                         price_range=price_range,
                         sort_by=sort_by)

@bp.route('/compare', methods=['GET', 'POST'])
def compare():
    """Phone comparison page"""
    if request.method == 'POST':
        phone1_id = request.form.get('phone1_id', type=int)
        phone2_id = request.form.get('phone2_id', type=int)

        if not phone1_id or not phone2_id:
            flash('Please select two phones to compare.', 'warning')
            return redirect(url_for('phone.compare'))

        if phone1_id == phone2_id:
            flash('Please select two different phones to compare.', 'warning')
            return redirect(url_for('phone.compare'))

        # Perform comparison
        comparison_engine = PhoneComparison()
        user_id = current_user.id if current_user.is_authenticated else None
        comparison_data = comparison_engine.compare_phones(phone1_id, phone2_id, user_id)

        if not comparison_data:
            flash('Unable to compare selected phones.', 'danger')
            return redirect(url_for('phone.compare'))

        return render_template('phone/compare_result.html',
                             comparison=comparison_data)

    # GET request - show comparison selection
    phone1_id = request.args.get('phone1', type=int)
    phone2_id = request.args.get('phone2', type=int)

    # If both phones provided in URL, perform comparison
    if phone1_id and phone2_id:
        comparison_engine = PhoneComparison()
        user_id = current_user.id if current_user.is_authenticated else None
        comparison_data = comparison_engine.compare_phones(phone1_id, phone2_id, user_id)

        if comparison_data:
            return render_template('phone/compare_result.html',
                                 comparison=comparison_data)

    # Get all active phones for selection
    phones = Phone.query.filter_by(is_active=True).order_by(Phone.model_name).all()
    brands = Brand.query.filter_by(is_active=True).order_by(Brand.name).all()

    return render_template('phone/compare.html',
                         phones=phones,
                         brands=brands,
                         phone1_id=phone1_id,
                         phone2_id=phone2_id)

@bp.route('/compare/history')
@login_required
def comparison_history():
    """View comparison history"""
    comparison_engine = PhoneComparison()
    comparisons = comparison_engine.get_user_comparisons(current_user.id, limit=20)

    return render_template('phone/comparison_history.html',
                         comparisons=comparisons)

@bp.route('/compare/save/<int:comparison_id>')
@login_required
def save_comparison(comparison_id):
    """Save a comparison"""
    comparison_engine = PhoneComparison()
    if comparison_engine.save_comparison(comparison_id):
        flash('Comparison saved successfully.', 'success')
    else:
        flash('Unable to save comparison.', 'danger')

    return redirect(url_for('phone.comparison_history'))

@bp.route('/search')
def search():
    """Search phones"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    if not query:
        return redirect(url_for('user.browse'))

    # Search in model name AND brand name
    from sqlalchemy import or_
    phones = Phone.query.join(Brand).filter(
        Phone.is_active == True,
        or_(
            Phone.model_name.ilike(f'%{query}%'),
            Brand.name.ilike(f'%{query}%')
        )
    ).paginate(page=page, per_page=12, error_out=False)

    return render_template('phone/search_results.html',
                         phones=phones,
                         query=query)
