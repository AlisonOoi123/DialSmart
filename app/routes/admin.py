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
from app.utils.email import send_contact_reply
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

    # Today's recommendations
    today = datetime.utcnow().date()
    today_recommendations = Recommendation.query.filter(
        db.func.date(Recommendation.created_at) == today
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

    # Get popular phones (most recommended)
    popular_phones = db.session.query(
        Phone,
        db.func.count(Recommendation.id).label('recommendation_count')
    ).join(Recommendation).group_by(Phone.id)\
     .order_by(db.func.count(Recommendation.id).desc())\
     .limit(5)\
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
            availability_status=availability_status
        )

        # Handle image upload
        if 'main_image' in request.files:
            file = request.files['main_image']
            if file.filename:
                filename = save_uploaded_file(file, 'phones')
                if filename:
                    phone.main_image = f'/static/uploads/phones/{filename}'

        db.session.add(phone)
        db.session.flush()  # Get phone ID

        # Create specifications
        specs = PhoneSpecification(
            phone_id=phone.id,
            screen_size=request.form.get('screen_size', type=float),
            screen_resolution=request.form.get('screen_resolution'),
            screen_type=request.form.get('screen_type'),
            refresh_rate=request.form.get('refresh_rate', type=int),
            processor=request.form.get('processor'),
            processor_brand=request.form.get('processor_brand'),
            ram_options=request.form.get('ram_options'),
            storage_options=request.form.get('storage_options'),
            expandable_storage=bool(request.form.get('expandable_storage')),
            rear_camera=request.form.get('rear_camera'),
            rear_camera_main=request.form.get('rear_camera_main', type=int),
            front_camera=request.form.get('front_camera'),
            front_camera_mp=request.form.get('front_camera_mp', type=int),
            battery_capacity=request.form.get('battery_capacity', type=int),
            charging_speed=request.form.get('charging_speed'),
            wireless_charging=bool(request.form.get('wireless_charging')),
            has_5g=bool(request.form.get('has_5g')),
            wifi_standard=request.form.get('wifi_standard'),
            bluetooth_version=request.form.get('bluetooth_version'),
            nfc=bool(request.form.get('nfc')),
            operating_system=request.form.get('operating_system'),
            fingerprint_sensor=bool(request.form.get('fingerprint_sensor')),
            face_unlock=bool(request.form.get('face_unlock')),
            water_resistance=request.form.get('water_resistance'),
            dual_sim=bool(request.form.get('dual_sim')),
            weight=request.form.get('weight', type=int),
            dimensions=request.form.get('dimensions'),
            colors_available=request.form.get('colors_available')
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
        phone.is_active = bool(request.form.get('is_active', True))

        # Handle image upload
        if 'main_image' in request.files:
            file = request.files['main_image']
            if file.filename:
                filename = save_uploaded_file(file, 'phones')
                if filename:
                    phone.main_image = f'/static/uploads/phones/{filename}'

        # Update specifications
        if not specs:
            specs = PhoneSpecification(phone_id=phone_id)
            db.session.add(specs)

        specs.screen_size = request.form.get('screen_size', type=float)
        specs.screen_resolution = request.form.get('screen_resolution')
        specs.screen_type = request.form.get('screen_type')
        specs.refresh_rate = request.form.get('refresh_rate', type=int)
        specs.processor = request.form.get('processor')
        specs.processor_brand = request.form.get('processor_brand')
        specs.ram_options = request.form.get('ram_options')
        specs.storage_options = request.form.get('storage_options')
        specs.expandable_storage = bool(request.form.get('expandable_storage'))
        specs.rear_camera = request.form.get('rear_camera')
        specs.rear_camera_main = request.form.get('rear_camera_main', type=int)
        specs.front_camera = request.form.get('front_camera')
        specs.front_camera_mp = request.form.get('front_camera_mp', type=int)
        specs.battery_capacity = request.form.get('battery_capacity', type=int)
        specs.charging_speed = request.form.get('charging_speed')
        specs.wireless_charging = bool(request.form.get('wireless_charging'))
        specs.has_5g = bool(request.form.get('has_5g'))
        specs.wifi_standard = request.form.get('wifi_standard')
        specs.bluetooth_version = request.form.get('bluetooth_version')
        specs.nfc = bool(request.form.get('nfc'))
        specs.operating_system = request.form.get('operating_system')
        specs.fingerprint_sensor = bool(request.form.get('fingerprint_sensor'))
        specs.face_unlock = bool(request.form.get('face_unlock'))
        specs.water_resistance = request.form.get('water_resistance')
        specs.dual_sim = bool(request.form.get('dual_sim'))
        specs.weight = request.form.get('weight', type=int)
        specs.dimensions = request.form.get('dimensions')
        specs.colors_available = request.form.get('colors_available')

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

# Message Management
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

    return render_template('admin/message_detail.html', message=message)

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

    # Send email reply
    try:
        # Get admin name for email signature
        admin_name = current_user.full_name if hasattr(current_user, 'full_name') and current_user.full_name else current_user.username

        # Send the email
        email_sent = send_contact_reply(
            user_email=message.email,
            user_name=message.name,
            original_subject=message.subject or "Your message to DialSmart",
            reply_text=reply_text,
            admin_name=admin_name
        )

        if email_sent:
            message.mark_as_replied()
            db.session.commit()
            flash(f'Reply sent to {message.email} successfully!', 'success')
        else:
            flash(f'Failed to send email to {message.email}. Please check email configuration.', 'warning')
            # Still mark as replied in database even if email fails
            message.mark_as_replied()
            db.session.commit()

    except Exception as e:
        flash(f'Error sending reply: {str(e)}', 'danger')
        db.session.rollback()

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

# Admin Registration (requires special registration code)
@bp.route('/register', methods=['GET', 'POST'])
def register_admin():
    """Register new admin with validation"""
    # If user is already logged in and is admin, redirect to dashboard
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        registration_code = request.form.get('registration_code', '').strip()

        # Validation
        errors = []

        # Check registration code (you should change this in production)
        # TODO: Store this in environment variable or database
        ADMIN_REGISTRATION_CODE = "DIALSMART_ADMIN_2025"
        if registration_code != ADMIN_REGISTRATION_CODE:
            errors.append('Invalid registration code. Contact system administrator.')

        # Validate username
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long.')

        if User.query.filter_by(username=username).first():
            errors.append('Username already exists.')

        # Validate email
        if not email or '@' not in email:
            errors.append('Please provide a valid email address.')

        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')

        # Validate password
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters long.')

        if password != confirm_password:
            errors.append('Passwords do not match.')

        # If there are errors, show them and return
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('admin/register.html')

        # Create new admin user
        try:
            new_admin = User(
                username=username,
                email=email,
                full_name=request.form.get('full_name', username),
                is_admin=True,
                is_active=True
            )
            new_admin.set_password(password)

            db.session.add(new_admin)
            db.session.commit()

            flash(f'Admin account created successfully for {username}! Please login.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating admin account: {str(e)}', 'danger')
            return render_template('admin/register.html')

    # GET request - show registration form
    return render_template('admin/register.html')

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
