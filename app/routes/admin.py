"""
Admin Routes
Admin panel for managing phones, brands, users, and system
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import User, Phone, PhoneSpecification, Brand, Recommendation, AuditLog, ContactMessage
from app.utils.helpers import save_uploaded_file, validate_password
from app.utils.email import send_user_suspended_email, send_user_activated_email
from datetime import datetime, timedelta
import json
import secrets

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


def log_audit_action(action_type, description, target_user_id=None, metadata=None):
    """Helper function to log audit actions"""
    try:
        audit_log = AuditLog(
            user_id=current_user.id if current_user.is_authenticated else None,
            target_user_id=target_user_id,
            action_type=action_type,
            description=description,
            ip_address=request.remote_addr if request else None,
            user_agent=request.headers.get('User-Agent')[:255] if request else None,
            chat_metadata=json.dumps(metadata) if metadata else None
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        # Log error but don't fail the main operation
        print(f"Error logging audit action: {e}")
        db.session.rollback()

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
    # Oracle uses TRUNC() instead of DATE() to extract date from timestamp
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

    # Get popular phones (most recommended)
    # Oracle doesn't allow CLOB/Text columns in GROUP BY, so we use a subquery approach
    # First, get phone IDs and their recommendation counts
    phone_counts_subquery = db.session.query(
        Recommendation.phone_id,
        db.func.count(Recommendation.id).label('recommendation_count')
    ).group_by(Recommendation.phone_id)\
     .order_by(db.func.count(Recommendation.id).desc())\
     .limit(5)\
     .subquery()

    # Then join with Phone table to get full phone objects
    popular_phones = db.session.query(
        Phone,
        phone_counts_subquery.c.recommendation_count
    ).join(
        phone_counts_subquery,
        Phone.id == phone_counts_subquery.c.phone_id
    ).order_by(phone_counts_subquery.c.recommendation_count.desc())\
     .all()

    # If no recommendations yet, show recently added phones instead
    if not popular_phones:
        recent_phones = Phone.query.filter_by(is_active=True)\
            .order_by(Phone.created_at.desc())\
            .limit(5)\
            .all()
        # Format to match popular_phones structure (phone, count)
        popular_phones = [(phone, 0) for phone in recent_phones]

    # Get unread contact messages count (Oracle uses 0 for false, 1 for true)
    unread_messages = ContactMessage.query.filter(
        (ContactMessage.is_read == 0) | (ContactMessage.is_read == None)
    ).count()

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

        # Release date
        release_date_str = request.form.get('release_date')
        release_date = None
        if release_date_str:
            try:
                release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid release date format.', 'warning')

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
            release_date=release_date
        )

        # Handle image upload
        if 'main_image' in request.files:
            main_image_url = request.form.get('main_image_url')
        if main_image_url:
            phone.main_image = main_image_url
        elif 'main_image' in request.files:
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
            colors_available=request.form.get('colors_available'),
            product_url=request.form.get('product_url')
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
            # Release date
            release_date_str = request.form.get('release_date')
        if release_date_str:
            try:
                phone.release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid release date format.', 'warning')

        # Handle image - prioritize URL over file upload
        main_image_url = request.form.get('main_image_url')
        if main_image_url:
            phone.main_image = main_image_url
        elif 'main_image' in request.files:
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
        specs.product_url = request.form.get('product_url')

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
        website_url = request.form.get('official_website')
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
            website_url=website_url,
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
        brand.website_url = request.form.get('website_url')
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
    """Delete brand"""
    brand = Brand.query.get_or_404(brand_id)
    brand_name = brand.name

    # Check if brand has associated phones
    phone_count = Phone.query.filter_by(brand_id=brand_id).count()
    if phone_count > 0:
        flash(f'Cannot delete brand "{brand_name}". It has {phone_count} associated phone(s). Please delete or reassign the phones first.', 'danger')
        return redirect(url_for('admin.brands'))

    db.session.delete(brand)
    db.session.commit()

    flash(f'Brand "{brand_name}" deleted successfully.', 'success')
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
    
    # Send email notification
    try:
        if user.is_active:
            send_user_activated_email(user)
        else:
            send_user_suspended_email(user)
        flash(f'User "{user.full_name}" has been {status}. Email notification sent.', 'success')
    except Exception as e:
        flash(f'User "{user.full_name}" has been {status}, but email notification failed to send.', 'warning')

    log_audit_action(
        action_type='user_status_changed',
        description=f'User {user.full_name} ({user.email}) {status}',
        target_user_id=user.id,
        metadata={'new_status': user.is_active}
    )

    return redirect(url_for('admin.users'))

# Admin Management
@bp.route('/admins')
@login_required
@admin_required
def admins():
    """List all admin users"""
    page = request.args.get('page', 1, type=int)
    admins = User.query.filter_by(is_admin=True)\
        .order_by(User.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/admins.html', admins=admins)

@bp.route('/admins/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_admin():
    """Create new admin user (requires passkey verification)"""
    # Admin passkey - MUST match the one in auth.py
    ADMIN_PASSKEY = "DialSmart2024Admin!"

    if request.method == 'POST':
        # Verify admin passkey FIRST
        admin_passkey = request.form.get('admin_passkey')

        if admin_passkey != ADMIN_PASSKEY:
            flash('Invalid admin passkey! Admin creation denied.', 'danger')
            log_audit_action(
                action_type='admin_creation_failed',
                description=f'Failed admin creation attempt - invalid passkey',
                metadata={'reason': 'invalid_passkey'}
            )
            return render_template('admin/create_admin.html')

        # Passkey verified - proceed with creation
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        temporary_password = request.form.get('temporary_password')

        # Validation
        if not all([full_name, email, temporary_password]):
            flash('All fields are required.', 'danger')
            return render_template('admin/create_admin.html')

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'warning')
            return render_template('admin/create_admin.html')

        # Validate password strength
        is_valid, error_message = validate_password(temporary_password)
        if not is_valid:
            flash(error_message, 'danger')
            return render_template('admin/create_admin.html')

        # Create new admin user
        new_admin = User(
            full_name=full_name,
            email=email,
            user_category='Admin',
            is_admin=True,
            force_password_change=True,  # Force password change on first login
            created_by_admin_id=current_user.id  # Track who created this admin
        )
        new_admin.set_password(temporary_password)

        db.session.add(new_admin)
        db.session.commit()

        # Log admin creation
        log_audit_action(
            action_type='admin_created',
            description=f'New admin created: {new_admin.full_name} ({new_admin.email}) by {current_user.full_name}',
            target_user_id=new_admin.id,
            metadata={
                'created_by': current_user.email,
                'created_admin_email': new_admin.email
            }
        )

        flash(f'Admin "{new_admin.full_name}" created successfully! They will be required to change password on first login.', 'success')
        return redirect(url_for('admin.admins'))

    return render_template('admin/create_admin.html')

@bp.route('/admins/<int:admin_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_admin(admin_id):
    """Delete admin user (requires passkey verification)"""
    if admin_id == current_user.id:
        flash('You cannot delete your own admin account.', 'danger')
        return redirect(url_for('admin.admins'))

    admin = User.query.get_or_404(admin_id)

    if not admin.is_admin:
        flash('This user is not an admin.', 'warning')
        return redirect(url_for('admin.admins'))

    # Verify passkey
    admin_passkey = request.form.get('admin_passkey')
    ADMIN_PASSKEY = "DialSmart2024Admin!"

    if admin_passkey != ADMIN_PASSKEY:
        flash('Invalid admin passkey! Admin deletion denied.', 'danger')
        log_audit_action(
            action_type='admin_deletion_failed',
            description=f'Failed admin deletion attempt for {admin.full_name} - invalid passkey',
            target_user_id=admin.id,
            metadata={'reason': 'invalid_passkey'}
        )
        return redirect(url_for('admin.admins'))

    # Log before deletion
    log_audit_action(
        action_type='admin_deleted',
        description=f'Admin deleted: {admin.full_name} ({admin.email}) by {current_user.full_name}',
        target_user_id=admin.id,
        metadata={
            'deleted_by': current_user.email,
            'deleted_admin_email': admin.email
        }
    )

    admin_name = admin.full_name
    db.session.delete(admin)
    db.session.commit()

    flash(f'Admin "{admin_name}" has been deleted.', 'success')
    return redirect(url_for('admin.admins'))

# Audit Logs
@bp.route('/audit-logs')
@login_required
@admin_required
def audit_logs():
    """View audit logs for admin actions"""
    page = request.args.get('page', 1, type=int)
    action_type = request.args.get('action_type', '')

    query = AuditLog.query

    if action_type:
        query = query.filter_by(action_type=action_type)

    logs = query.order_by(AuditLog.created_at.desc())\
        .paginate(page=page, per_page=50, error_out=False)

    # Get unique action types for filter
    action_types = db.session.query(AuditLog.action_type.distinct()).all()
    action_types = [t[0] for t in action_types]

    return render_template('admin/audit_logs.html',
                         logs=logs,
                         action_types=action_types,
                         current_action_type=action_type)

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

# Contact Messages
@bp.route('/messages')
@login_required
@admin_required
def messages():
    """View all contact messages"""
    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('filter', 'all')  # all, unread, replied

    query = ContactMessage.query

    # Oracle uses 0 for false, 1 for true
    if filter_type == 'unread':
        query = query.filter((ContactMessage.is_read == 0) | (ContactMessage.is_read == None))
    elif filter_type == 'replied':
        query = query.filter(ContactMessage.is_replied == 1)
    elif filter_type == 'pending':
        query = query.filter((ContactMessage.is_replied == 0) | (ContactMessage.is_replied == None))

    messages = query.order_by(ContactMessage.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)

    # Get counts for filters
    total_count = ContactMessage.query.count()
    unread_count = ContactMessage.query.filter(
        (ContactMessage.is_read == 0) | (ContactMessage.is_read == None)
    ).count()
    pending_count = ContactMessage.query.filter(
        (ContactMessage.is_replied == 0) | (ContactMessage.is_replied == None)
    ).count()

    return render_template('admin/messages.html',
                         messages=messages,
                         filter_type=filter_type,
                         total_count=total_count,
                         unread_count=unread_count,
                         pending_count=pending_count)

@bp.route('/messages/<int:message_id>')
@login_required
@admin_required
def message_details(message_id):
    """View message details"""
    message = ContactMessage.query.get_or_404(message_id)

    # Mark as read
    if not message.is_read:
        message.mark_as_read()

    return render_template('admin/message_details.html', message=message)

@bp.route('/messages/<int:message_id>/reply', methods=['POST'])
@login_required
@admin_required
def reply_message(message_id):
    """Reply to a contact message"""
    from app.utils.email import send_admin_reply_email

    message = ContactMessage.query.get_or_404(message_id)
    reply_text = request.form.get('reply')

    if not reply_text:
        flash('Reply message cannot be empty.', 'danger')
        return redirect(url_for('admin.message_details', message_id=message_id))

    # Save reply to database first (regardless of email success)
    message.mark_as_replied(current_user, reply_text)

    # Try to send email notification
    success, email_message = send_admin_reply_email(
        user_email=message.email,
        user_name=message.name,
        reply_message=reply_text,
        original_message=message.message
    )

    if success:
        flash('Reply saved and sent successfully via email.', 'success')
    else:
        flash(f'Reply saved to database, but email failed: {email_message}. Please configure email settings in .env file.', 'warning')

    return redirect(url_for('admin.message_details', message_id=message_id))

@bp.route('/messages/<int:message_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_message(message_id):
    """Delete a contact message"""
    message = ContactMessage.query.get_or_404(message_id)

    db.session.delete(message)
    db.session.commit()

    flash('Message deleted successfully.', 'success')
    return redirect(url_for('admin.messages'))
