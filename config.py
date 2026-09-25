import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'employeehub-dev-secret-key-change-in-prod-2026')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=4)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database config: default to MySQL, fallback to SQLite if specified or in testing
    # Format: mysql+pymysql://username:password@host:port/database_name
    DEFAULT_MYSQL_URL = 'mysql+pymysql://root:password@localhost:3306/employeehub_db'
    
    # Retrieve DATABASE_URL from environment (e.g. Render, Railway, or local .env)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Support Render's postgres:// -> postgresql:// or mysql:// -> mysql+pymysql://
    if DATABASE_URL:
        if DATABASE_URL.startswith("mysql://"):
            DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
        elif DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback to local SQLite if USE_SQLITE is set, else MySQL default
        if os.environ.get('USE_SQLITE', 'false').lower() in ('true', '1', 'yes'):
            SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'employeehub.db')}"
        else:
            SQLALCHEMY_DATABASE_URI = DEFAULT_MYSQL_URL

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    # Fast in-memory SQLite for reliable isolated tests & CI pipelines
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'
    # In production, ensure SECRET_KEY is set via env var
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-secret-fallback-key-must-override')

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
