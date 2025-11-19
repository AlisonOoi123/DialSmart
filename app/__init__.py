"""
DialSmart Application Factory
Initializes and configures the Flask application
"""
from flask import Flask, session, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
from config import config
import os
from datetime import datetime
import pytz

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    mail.init_app(app)

    # Register custom Jinja2 filters
    @app.template_filter('local_time')
    def local_time_filter(dt, format='%Y-%m-%d %H:%M:%S'):
        """Convert UTC datetime to local time and format it"""
        if dt is None:
            return ''

        # If datetime is naive, assume it's UTC
        if dt.tzinfo is None:
            dt = pytz.UTC.localize(dt)

        # Convert to Malaysia timezone (UTC+8)
        malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
        local_dt = dt.astimezone(malaysia_tz)

        return local_dt.strftime(format)

    @app.template_filter('format_date')
    def format_date_filter(dt, format='%d %b %Y'):
        """Format date"""
        if dt is None:
            return ''
        if isinstance(dt, datetime):
            return dt.strftime(format)
        return str(dt)

    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.routes import auth, user, admin, phone, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(phone.bp)
    app.register_blueprint(api.bp)

    # Register context processors
    @app.context_processor
    def inject_brands():
        """Inject featured brands into all templates"""
        return dict(featured_brands=app.config['FEATURED_BRANDS'])
    
    @app.after_request
    def add_security_headers(response):
        """
        Add cache control headers to prevent browser caching of authenticated pages.
        This prevents users from using the back button to access protected pages after logout.
        """
        # Protected route prefixes that should never be cached
        protected_prefixes = ('/dashboard', '/admin', '/auth/logout', '/user/', '/phone/compare')

        # Apply cache headers to:
        # 1. Currently authenticated users (for all their pages)
        # 2. Protected routes (even if user is not currently authenticated - prevents forward button)
        # 3. But NOT to static files or public pages
        is_protected = any(request.path.startswith(prefix) for prefix in protected_prefixes)

        # Only apply to authenticated user pages (not public pages or static files)
        if (current_user.is_authenticated or is_protected) and not request.path.startswith('/static'):
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
