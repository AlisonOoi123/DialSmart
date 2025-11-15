"""
DialSmart Configuration File
Manages all application settings and configurations
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dialsmart-secret-key-2024'

    # Database settings
    # Options: SQLite (development), MySQL (recommended), PostgreSQL (advanced)
    #
    # For MySQL, set environment variable DATABASE_URL to:
    # mysql+pymysql://username:password@localhost/dialsmart
    #
    # Or edit the default below directly
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # MySQL connection (recommended for production)
    # Change these values to match your MySQL setup:
    MYSQL_USER = os.environ.get('MYSQL_USER', 'dialsmart_user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'dialsmart123')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'dialsmart')

    # Database URI - Change USE_MYSQL to switch databases
    USE_MYSQL = os.environ.get('USE_MYSQL', 'false').lower() == 'true'

    if USE_MYSQL:
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'
    else:
        # SQLite (development only)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dialsmart.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
    }

    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Pagination
    ITEMS_PER_PAGE = 12
    ADMIN_ITEMS_PER_PAGE = 20

    # AI Model settings
    AI_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'recommendation_model.pkl')

    # Malaysian Ringgit price ranges
    PRICE_RANGES = {
        'budget': (0, 1000),
        'mid_range': (1000, 2000),
        'upper_mid': (2000, 3000),
        'premium': (3000, 10000)
    }

    # Featured brands (from CSV dataset + popular brands)
    FEATURED_BRANDS = [
        'Samsung', 'Apple', 'Xiaomi', 'Oppo', 'Vivo', 'Realme',
        'Honor', 'Huawei', 'Google', 'Asus', 'Poco', 'Redmi', 'Infinix'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
