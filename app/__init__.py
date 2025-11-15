"""
DialSmart Application Factory
Initializes and configures the Flask application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import os
import click

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Enable Oracle thick mode for Oracle 11g compatibility
    if app.config.get('DB_TYPE') == 'oracle':
        try:
            import oracledb
            # Initialize thick mode (required for Oracle 11g)
            # This uses the Oracle Client libraries that come with Oracle installation
            oracledb.init_oracle_client()
        except Exception as e:
            # If thick mode initialization fails, provide helpful error
            print(f"Warning: Oracle thick mode initialization failed: {e}")
            print("Oracle 11g requires thick mode. Make sure Oracle is installed.")

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

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
