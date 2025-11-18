"""
DialSmart Application Factory
Initializes and configures the Flask application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
