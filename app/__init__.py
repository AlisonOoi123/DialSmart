"""
DialSmart Application Factory
Initializes and configures the Flask application
"""
from flask import Flask, session, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

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

    # Add security headers to prevent back button access after logout
    @app.after_request
    def add_security_headers(response):
        """
        Add cache control headers to prevent browser caching of authenticated pages.
        This prevents users from using the back/forward button to access protected pages after logout.

        CRITICAL: Must apply to protected routes regardless of current authentication status,
        otherwise forward button after logout will still show cached authenticated pages.
        """
        # Protected route prefixes that should never be cached
        protected_prefixes = ('/dashboard', '/admin', '/auth/logout', '/user/', '/phone/compare')

        # Apply cache headers to:
        # 1. Currently authenticated users (for all their pages)
        # 2. Protected routes (even if user is not currently authenticated - prevents forward button)
        # 3. But NOT to static files or public pages
        is_protected = any(request.path.startswith(prefix) for prefix in protected_prefixes)

        if (current_user.is_authenticated or is_protected) and not request.path.startswith('/static'):
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'

        return response

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
