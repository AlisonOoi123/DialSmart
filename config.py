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
    # Default: SQLite (good for development)
    # Production: Set DATABASE_URL environment variable to PostgreSQL
    # Example: postgresql://user:password@localhost/dialsmart
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'dialsmart.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
