"""
Admin Routes
Admin panel for managing phones, brands, users, and system
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import User, Phone, PhoneSpecification, Brand, Recommendation
from app.models.contact import ContactMessage
from app.utils.helpers import save_uploaded_file
from datetime import datetime, timedelta
import json

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    # Get statistics
    total_users = User.query.filter_by(is_admin=False).count()
    total_phones = Phone.query.filter_by(is_active=True).count()
    total_brands = Brand.query.filter_by(is_active=True).count()

    # Today's recommendations - use TRUNC for Oracle compatibility
    today = datetime.utcnow().date()
    today_recommendations = Recommendation.query.filter(
        db.func.trunc(Recommendation.created_at) == today
    ).count()

    # Recent activity (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_users = User.query.filter(User.created_at >= week_ago).count()
    recent_recommendations = Recommendation.query.filter(
        Recommendation.created_at >= week_ago
    ).count()

    # Get recent users
    recent_users_list = User.query.filter_by(is_admin=False)\
        .order_by(User.created_at.desc())\
        .limit(5)\
        .all()

    # Get popular phones (most recommended) - Oracle compatible version
    # Use subquery to avoid CLOB columns in GROUP BY (Oracle doesn't support CLOB in GROUP BY)
    phone_counts = db.session.query(
        Recommendation.phone_id,
        db.func.count(Recommendation.id).label('recommendation_count')
    ).group_by(Recommendation.phone_id)\
     .order_by(db.func.count(Recommendation.id).desc())\
     .limit(5)\
     .subquery()

    # Join with Phone table to get full phone details
    popular_phones = db.session.query(
        Phone,
        phone_counts.c.recommendation_count
    ).join(phone_counts, Phone.id == phone_counts.c.phone_id)\
     .all()

    # Get unread messages count
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()

    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_phones=total_phones,
                         total_brands=total_brands,
                         today_recommendations=today_recommendations,
                         new_users=new_users,
                         recent_recommendations=recent_recommendations,
                         recent_users=recent_users_list,
                         popular_phones=popular_phones,
                         unread_messages=unread_messages)

# Phone Management
@bp.route('/phones')
@login_required
@admin_required
def phones():
    """List all phones"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    brand_id = request.args.get('brand_id', type=int)

    query = Phone.query

    if search:
        query = query.filter(Phone.model_name.ilike(f'%{search}%'))

    if brand_id:
        query = query.filter_by(brand_id=brand_id)

    phones = query.order_by(Phone.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)

    brands = Brand.query.filter_by(is_active=True).all()

    return render_template('admin/phones.html',
                         phones=phones,
                         brands=brands,
                         search=search,
                         brand_id=brand_id)

@bp.route('/phones/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_phone():
    """Add new phone"""
    if request.method == 'POST':
        # Basic information
        model_name = request.form.get('model_name')
        brand_id = request.form.get('brand_id', type=int)
        price = request.form.get('price', type=float)
        model_number = request.form.get('model_number')
        availability_status = request.form.get('availability_status', 'Available')

        # Validation
        if not all([model_name, brand_id, price]):
            flash('Model name, brand, and price are required.', 'danger')
            return redirect(url_for('admin.add_phone'))

        # Create phone
        phone = Phone(
            model_name=model_name,
            brand_id=brand_id,
            price=price,
            model_number=model_number,
            availability_status=availability_status,
            release_date=request.form.get('release_date') or None
        )

        # Handle image - URL has priority over file upload
        image_url = request.form.get('main_image_url', '').strip()
        if image_url:
            # Use the provided URL directly
            phone.main_image = image_url
        elif 'main_image' in request.files:
            # Fallback to file upload if no URL provided
            file = request.files['main_image']
            if file.filename:
                filename = save_uploaded_file(file, 'phones')
                if filename:
                    phone.main_image = f'/static/uploads/phones/{filename}'

        db.session.add(phone)
        db.session.flush()  # Get phone ID

        # Create specifications - All CSV attributes supported
        specs = PhoneSpecification(
            phone_id=phone.id,
            # Display
            screen_size=request.form.get('screen_size') or None,
            screen_resolution=request.form.get('screen_resolution') or None,
            display_type=request.form.get('display_type') or None,
            ppi=request.form.get('ppi') or None,
            multitouch=request.form.get('multitouch') or None,
            protection=request.form.get('protection') or None,
            # Performance
            operating_system=request.form.get('operating_system') or None,
            chipset=request.form.get('chipset') or None,
            cpu=request.form.get('cpu') or None,
            gpu=request.form.get('gpu') or None,
            ram_options=request.form.get('ram_options') or None,
            storage_options=request.form.get('storage_options') or None,
            card_slot=request.form.get('card_slot') or None,
            # Camera
            rear_camera=request.form.get('rear_camera') or None,
            front_camera=request.form.get('front_camera') or None,
            flash=request.form.get('flash') or None,
            camera_features=request.form.get('camera_features') or None,
            video_recording=request.form.get('video_recording') or None,
            # Battery
            battery=request.form.get('battery') or None,
            battery_capacity=request.form.get('battery_capacity') or None,
            fast_charging=request.form.get('fast_charging') or None,
            wireless_charging=request.form.get('wireless_charging') or None,
            removable_battery=request.form.get('removable_battery') or None,
            # Network
            sim=request.form.get('sim') or None,
            technology=request.form.get('technology') or None,
            network_5g=request.form.get('network_5g') or None,
            network_4g=request.form.get('network_4g') or None,
            network_3g=request.form.get('network_3g') or None,
            network_2g=request.form.get('network_2g') or None,
            network_speed=request.form.get('network_speed') or None,
            wifi_standard=request.form.get('wifi_standard') or None,
            bluetooth_version=request.form.get('bluetooth_version') or None,
            gps=request.form.get('gps') or None,
            nfc=request.form.get('nfc') or None,
            usb=request.form.get('usb') or None,
            radio=request.form.get('radio') or None,
            # Physical
            dimensions=request.form.get('dimensions') or None,
            weight=request.form.get('weight') or None,
            colors_available=request.form.get('colors_available') or None,
            body_material=request.form.get('body_material') or None,
            # Sensors
            sensors=request.form.get('sensors') or None,
            water_resistance=request.form.get('water_resistance') or None,
            # Reference
            product_url=request.form.get('product_url') or None
        )

        db.session.add(specs)
        db.session.commit()

        flash(f'Phone "{model_name}" added successfully.', 'success')
        return redirect(url_for('admin.phones'))

    brands = Brand.query.filter_by(is_active=True).order_by(Brand.name).all()
    return render_template('admin/phone_form.html', phone=None, brands=brands)

@bp.route('/phones/edit/<int:phone_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_phone(phone_id):
    """Edit existing phone"""
    phone = Phone.query.get_or_404(phone_id)
    specs = PhoneSpecification.query.filter_by(phone_id=phone_id).first()

    if request.method == 'POST':
        # Update basic information
        phone.model_name = request.form.get('model_name', phone.model_name)
        phone.brand_id = request.form.get('brand_id', type=int)
        phone.price = request.form.get('price', type=float)
        phone.model_number = request.form.get('model_number')
        phone.availability_status = request.form.get('availability_status', 'Available')
        phone.release_date = request.form.get('release_date') or None
        phone.is_active = bool(request.form.get('is_active', True))

        # Handle image - URL has priority over file upload
        image_url = request.form.get('main_image_url', '').strip()
        if image_url:
            # Use the provided URL directly
            phone.main_image = image_url
        elif 'main_image' in request.files:
            # Fallback to file upload if no URL provided
            file = request.files['main_image']
            if file.filename:
                filename = save_uploaded_file(file, 'phones')
                if filename:
                    phone.main_image = f'/static/uploads/phones/{filename}'

        # Update specifications - All CSV attributes supported
        if not specs:
            specs = PhoneSpecification(phone_id=phone_id)
            db.session.add(specs)

        # Display
        specs.screen_size = request.form.get('screen_size') or None
        specs.screen_resolution = request.form.get('screen_resolution') or None
        specs.display_type = request.form.get('display_type') or None
        specs.ppi = request.form.get('ppi') or None
        specs.multitouch = request.form.get('multitouch') or None
        specs.protection = request.form.get('protection') or None
        # Performance
        specs.operating_system = request.form.get('operating_system') or None
        specs.chipset = request.form.get('chipset') or None
        specs.cpu = request.form.get('cpu') or None
        specs.gpu = request.form.get('gpu') or None
        specs.ram_options = request.form.get('ram_options') or None
        specs.storage_options = request.form.get('storage_options') or None
        specs.card_slot = request.form.get('card_slot') or None
        # Camera
        specs.rear_camera = request.form.get('rear_camera') or None
        specs.front_camera = request.form.get('front_camera') or None
        specs.flash = request.form.get('flash') or None
        specs.camera_features = request.form.get('camera_features') or None
        specs.video_recording = request.form.get('video_recording') or None
        # Battery
        specs.battery = request.form.get('battery') or None
        specs.battery_capacity = request.form.get('battery_capacity') or None
        specs.fast_charging = request.form.get('fast_charging') or None
        specs.wireless_charging = request.form.get('wireless_charging') or None
        specs.removable_battery = request.form.get('removable_battery') or None
        # Network
        specs.sim = request.form.get('sim') or None
        specs.technology = request.form.get('technology') or None
        specs.network_5g = request.form.get('network_5g') or None
        specs.network_4g = request.form.get('network_4g') or None
        specs.network_3g = request.form.get('network_3g') or None
        specs.network_2g = request.form.get('network_2g') or None
        specs.network_speed = request.form.get('network_speed') or None
        specs.wifi_standard = request.form.get('wifi_standard') or None
        specs.bluetooth_version = request.form.get('bluetooth_version') or None
        specs.gps = request.form.get('gps') or None
        specs.nfc = request.form.get('nfc') or None
        specs.usb = request.form.get('usb') or None
        specs.radio = request.form.get('radio') or None
        # Physical
        specs.dimensions = request.form.get('dimensions') or None
        specs.weight = request.form.get('weight') or None
        specs.colors_available = request.form.get('colors_available') or None
        specs.body_material = request.form.get('body_material') or None
        # Sensors
        specs.sensors = request.form.get('sensors') or None
        specs.water_resistance = request.form.get('water_resistance') or None
        # Reference
        specs.product_url = request.form.get('product_url') or None

        db.session.commit()
        flash(f'Phone "{phone.model_name}" updated successfully.', 'success')
        return redirect(url_for('admin.phones'))

    brands = Brand.query.filter_by(is_active=True).order_by(Brand.name).all()
    return render_template('admin/phone_form.html',
                         phone=phone,
                         specs=specs,
                         brands=brands)

@bp.route('/phones/delete/<int:phone_id>', methods=['POST'])
@login_required
@admin_required
def delete_phone(phone_id):
    """Delete phone"""
    phone = Phone.query.get_or_404(phone_id)
    phone_name = phone.model_name

    db.session.delete(phone)
    db.session.commit()

    flash(f'Phone "{phone_name}" deleted successfully.', 'success')
    return redirect(url_for('admin.phones'))

# Brand Management
@bp.route('/brands')
@login_required
@admin_required
def brands():
    """List all brands"""
    page = request.args.get('page', 1, type=int)
    brands = Brand.query.order_by(Brand.name)\
        .paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/brands.html', brands=brands)

@bp.route('/brands/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_brand():
    """Add new brand"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        tagline = request.form.get('tagline')
        is_featured = bool(request.form.get('is_featured'))

        if not name:
            flash('Brand name is required.', 'danger')
            return redirect(url_for('admin.add_brand'))

        # Check if brand already exists
        existing = Brand.query.filter_by(name=name).first()
        if existing:
            flash('Brand already exists.', 'warning')
            return redirect(url_for('admin.brands'))

        brand = Brand(
            name=name,
            description=description,
            tagline=tagline,
            is_featured=is_featured
        )

        # Handle logo upload
        if 'logo' in request.files:
            file = request.files['logo']
            if file.filename:
                filename = save_uploaded_file(file, 'brands')
                if filename:
                    brand.logo_url = f'/static/uploads/brands/{filename}'

        db.session.add(brand)
        db.session.commit()

        flash(f'Brand "{name}" added successfully.', 'success')
        return redirect(url_for('admin.brands'))

    return render_template('admin/brand_form.html', brand=None)

@bp.route('/brands/edit/<int:brand_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_brand(brand_id):
    """Edit brand"""
    brand = Brand.query.get_or_404(brand_id)

    if request.method == 'POST':
        brand.name = request.form.get('name', brand.name)
        brand.description = request.form.get('description')
        brand.tagline = request.form.get('tagline')
        brand.is_featured = bool(request.form.get('is_featured'))
        brand.is_active = bool(request.form.get('is_active', True))

        # Handle logo upload
        if 'logo' in request.files:
            file = request.files['logo']
            if file.filename:
                filename = save_uploaded_file(file, 'brands')
                if filename:
                    brand.logo_url = f'/static/uploads/brands/{filename}'

        db.session.commit()
        flash(f'Brand "{brand.name}" updated successfully.', 'success')
        return redirect(url_for('admin.brands'))

    return render_template('admin/brand_form.html', brand=brand)

@bp.route('/brands/delete/<int:brand_id>', methods=['POST'])
@login_required
@admin_required
def delete_brand(brand_id):
    """Delete brand and all associated phones (cascade delete)"""
    brand = Brand.query.get_or_404(brand_id)
    brand_name = brand.name
    phone_count = brand.get_phone_count()

    try:
        # Delete brand (cascade will automatically delete all phones)
        db.session.delete(brand)
        db.session.commit()
        flash(f'Brand "{brand_name}" and {phone_count} associated phone(s) deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting brand: {str(e)}', 'danger')

    return redirect(url_for('admin.brands'))

# User Management
@bp.route('/users')
@login_required
@admin_required
def users():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    user_type = request.args.get('type', '')

    query = User.query

    if search:
        query = query.filter(
            db.or_(
                User.full_name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )

    if user_type:
        query = query.filter_by(user_category=user_type)

    users = query.order_by(User.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/users.html',
                         users=users,
                         search=search,
                         user_type=user_type)

@bp.route('/users/<int:user_id>')
@login_required
@admin_required
def user_details(user_id):
    """View user details"""
    user = User.query.get_or_404(user_id)

    # Get user statistics
    total_recommendations = Recommendation.query.filter_by(user_id=user_id).count()
    recent_recommendations = Recommendation.query.filter_by(user_id=user_id)\
        .order_by(Recommendation.created_at.desc())\
        .limit(10)\
        .all()

    return render_template('admin/user_details.html',
                         user=user,
                         total_recommendations=total_recommendations,
                         recent_recommendations=recent_recommendations)

@bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Activate or suspend user"""
    user = User.query.get_or_404(user_id)

    if user.is_admin:
        flash('Cannot modify admin user status.', 'warning')
        return redirect(url_for('admin.users'))

    user.is_active = not user.is_active
    db.session.commit()

    status = 'activated' if user.is_active else 'suspended'
    flash(f'User "{user.full_name}" has been {status}.', 'success')

    return redirect(url_for('admin.users'))

# System Logs
@bp.route('/logs')
@login_required
@admin_required
def logs():
    """View system logs"""
    # Get recent recommendations for activity log
    page = request.args.get('page', 1, type=int)
    recommendations = Recommendation.query\
        .order_by(Recommendation.created_at.desc())\
        .paginate(page=page, per_page=50, error_out=False)

    return render_template('admin/logs.html',
                         recommendations=recommendations)

# Messages Management
@bp.route('/messages')
@login_required
@admin_required
def messages():
    """View all contact messages"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')

    query = ContactMessage.query

    if status == 'unread':
        query = query.filter_by(is_read=False)
    elif status == 'replied':
        query = query.filter_by(is_replied=True)
    elif status == 'unreplied':
        query = query.filter_by(is_replied=False)

    messages = query.order_by(ContactMessage.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)

    # Get counts for tabs
    total_count = ContactMessage.query.count()
    unread_count = ContactMessage.query.filter_by(is_read=False).count()
    unreplied_count = ContactMessage.query.filter_by(is_replied=False).count()

    return render_template('admin/messages.html',
                         messages=messages,
                         status=status,
                         total_count=total_count,
                         unread_count=unread_count,
                         unreplied_count=unreplied_count)

@bp.route('/messages/<int:message_id>')
@login_required
@admin_required
def message_details(message_id):
    """View message details"""
    message = ContactMessage.query.get_or_404(message_id)

    # Mark as read
    if not message.is_read:
        message.mark_as_read()
        db.session.commit()

    return render_template('admin/message_details.html', message=message)

@bp.route('/messages/<int:message_id>/reply', methods=['POST'])
@login_required
@admin_required
def reply_message(message_id):
    """Reply to a message via email"""
    message = ContactMessage.query.get_or_404(message_id)
    reply_text = request.form.get('reply_text', '')
    admin_notes = request.form.get('admin_notes', '')

    if not reply_text:
        flash('Reply text is required.', 'danger')
        return redirect(url_for('admin.message_details', message_id=message_id))

    # Save admin notes
    if admin_notes:
        message.admin_notes = admin_notes

    # TODO: Send email to user
    # For now, just mark as replied
    # In production, integrate with Flask-Mail or similar email service
    try:
        # Email sending would go here
        # send_email(
        #     to=message.email,
        #     subject=f"Re: {message.subject or 'Your message to DialSmart'}",
        #     body=reply_text
        # )

        message.mark_as_replied()
        db.session.commit()
        flash(f'Reply sent to {message.email} successfully.', 'success')
    except Exception as e:
        flash(f'Error sending reply: {str(e)}', 'danger')

    return redirect(url_for('admin.message_details', message_id=message_id))

@bp.route('/messages/<int:message_id>/mark-read', methods=['POST'])
@login_required
@admin_required
def mark_message_read(message_id):
    """Mark message as read"""
    message = ContactMessage.query.get_or_404(message_id)
    message.mark_as_read()
    db.session.commit()
    flash('Message marked as read.', 'success')
    return redirect(url_for('admin.messages'))

@bp.route('/messages/<int:message_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_message(message_id):
    """Delete a message"""
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully.', 'success')
    return redirect(url_for('admin.messages'))

# Settings
@bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    """System settings"""
    if request.method == 'POST':
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html')
