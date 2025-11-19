"""
Authentication Routes
Handles user registration, login, and logout
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.utils.helpers import validate_password
from datetime import datetime
from app.utils.email import send_verification_email, send_password_reset_email, is_token_expired

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Try to import email utilities, but handle if they don't exist
try:
    from app.utils.email import send_verification_email, send_password_reset_email, is_token_expired
    EMAIL_UTILS_AVAILABLE = True
except ImportError:
    EMAIL_UTILS_AVAILABLE = False

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_category = request.form.get('user_category')
        age_range = request.form.get('age_range')

        # Validation
        if not all([full_name, email, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        # Validate password strength
        is_valid, error_message = validate_password(password)
        if not is_valid:
            flash(error_message, 'danger')
            return render_template('auth/register.html')

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))

        # Create new user
        user = User(
            full_name=full_name,
            email=email,
            user_category=user_category,
            age_range=age_range
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Send verification email if enabled
        if current_app.config.get('EMAIL_VERIFICATION_REQUIRED'):
            success, message = send_verification_email(user)
            if success:
                db.session.commit()  # Save verification token
                flash('Registration successful! Please check your email to verify your account.', 'success')
            else:
                flash('Registration successful! However, we could not send the verification email. You can still login.', 'warning')
        else:
            # Auto-verify if email verification is disabled
            if hasattr(user, 'email_verified'):
                user.email_verified = True
                db.session.commit()
            flash('Registration successful! Please login.', 'success')

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been suspended. Please contact support.', 'danger')
                return render_template('auth/login.html')

            login_user(user, remember=remember)
            user.update_last_active()

            # Redirect based on user type
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('user.index'))

@bp.route('/register-admin', methods=['GET', 'POST'])
def register_admin():
    """Admin registration page with passkey protection"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))

    # Admin passkey - CHANGE THIS IN PRODUCTION!
    ADMIN_PASSKEY = "DialSmart2024Admin!"

    if request.method == 'POST':
        # Verify admin passkey first
        admin_passkey = request.form.get('admin_passkey')

        if admin_passkey != ADMIN_PASSKEY:
            flash('Invalid admin passkey! You cannot register as admin without the correct passkey.', 'danger')
            return render_template('auth/register.html', is_admin_registration=True)

        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not all([full_name, email, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html', is_admin_registration=True)

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html', is_admin_registration=True)

        # Validate password strength
        is_valid, error_message = validate_password(password)
        if not is_valid:
            flash(error_message, 'danger')
            return render_template('auth/register.html', is_admin_registration=True)

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'warning')
            return redirect(url_for('auth.login'))

        # Create new admin user
        user = User(
            full_name=full_name,
            email=email,
            user_category='Admin',
            is_admin=True
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Admin registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', is_admin_registration=True)

@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page - verifies email and sends reset link"""
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')

        # Check if email exists
        user = User.query.filter_by(email=email).first()

        if not user:
            # Email not registered - ask user to register
            flash('This email is not registered. Please register for an account first.', 'warning')
            return redirect(url_for('auth.register'))

        # Email exists - send password reset email
        success, message = send_password_reset_email(user)

        if success:
            db.session.commit()  # Save reset token
            flash('Password reset instructions have been sent to your email. Please check your inbox.', 'success')
            return redirect(url_for('auth.login'))
        else:
            # Email failed - generate reset link and show it directly (development fallback)
            current_app.logger.error(f"Failed to send reset email: {message}")

            # Generate token if not already generated
            if not user.password_reset_token:
                from app.utils.email import generate_secure_token
                user.password_reset_token = generate_secure_token()
                user.password_reset_sent_at = datetime.utcnow()
                db.session.commit()

            # Create reset URL
            reset_url = url_for('auth.reset_password', token=user.password_reset_token, _external=True)

            flash(f'Email service not configured. Use this link to reset your password: {reset_url}', 'warning')
            return redirect(url_for('auth.forgot_password'))

    return render_template('auth/forgot_password.html')

@bp.route('/verify-email/<token>')
def verify_email(token):
    """Verify user email with token"""
    user = User.query.filter_by(email_verification_token=token).first()

    if not user:
        flash('Invalid verification link.', 'danger')
        return redirect(url_for('auth.login'))

    # Check if token expired
    expiry_seconds = current_app.config.get('EMAIL_VERIFICATION_TOKEN_EXPIRY', 24 * 3600)
    if is_token_expired(user.email_verification_sent_at, expiry_seconds):
        flash('Verification link has expired. Please request a new one.', 'warning')
        return redirect(url_for('auth.resend_verification', email=user.email))

    # Verify the email
    user.email_verified = True
    user.email_verification_token = None
    user.email_verification_sent_at = None
    db.session.commit()

    flash('Email verified successfully! You can now login.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/resend-verification', methods=['GET', 'POST'])
def resend_verification():
    """Resend verification email"""
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Email not found.', 'danger')
            return render_template('auth/resend_verification.html')

        if user.email_verified:
            flash('Your email is already verified. Please login.', 'info')
            return redirect(url_for('auth.login'))

        # Resend verification email
        success, message = send_verification_email(user)
        if success:
            db.session.commit()
            flash('Verification email sent! Please check your inbox.', 'success')
        else:
            flash(f'Failed to send verification email. {message}', 'danger')

        return redirect(url_for('auth.login'))

    # GET request - show form
    email = request.args.get('email', '')
    return render_template('auth/resend_verification.html', email=email)

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    # Find user with this reset token
    user = User.query.filter_by(password_reset_token=token).first()

    if not user:
        flash('Invalid or expired password reset link.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    # Check if token expired (1 hour = 3600 seconds)
    if is_token_expired(user.password_reset_sent_at, 3600):
        flash('Password reset link has expired. Please request a new one.', 'warning')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not new_password or not confirm_password:
            flash('Both password fields are required.', 'danger')
            return render_template('auth/reset_password.html', token=token)

        if new_password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/reset_password.html', token=token)

        # Validate password strength
        is_valid, error_message = validate_password(new_password)
        if not is_valid:
            flash(error_message, 'danger')
            return render_template('auth/reset_password.html', token=token)

        # Reset the password
        user.set_password(new_password)
        user.password_reset_token = None
        user.password_reset_sent_at = None
        db.session.commit()

        flash('Password reset successful! You can now login with your new password.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)
