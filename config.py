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
    
    # Credentials from .env
    DEFAULT_ADMIN_NAME = os.environ.get('DEFAULT_ADMIN_NAME', 'System Administrator')
    DEFAULT_ADMIN_USERNAME = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
    DEFAULT_ADMIN_EMAIL = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@employeehub.com')
    DEFAULT_ADMIN_PASSWORD = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'admin123')
    
    DEFAULT_HR_NAME = os.environ.get('DEFAULT_HR_NAME', 'Sarah Jenkins')
    DEFAULT_HR_USERNAME = os.environ.get('DEFAULT_HR_USERNAME', 'hr_manager')
    DEFAULT_HR_EMAIL = os.environ.get('DEFAULT_HR_EMAIL', 'hr@employeehub.com')
    DEFAULT_HR_PASSWORD = os.environ.get('DEFAULT_HR_PASSWORD', 'hr123')
    
    # Construct MySQL URI from individual parameters if provided
    db_user = os.environ.get('DB_USER', 'root')
    db_pass = os.environ.get('DB_PASSWORD', 'password')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '3306')
    db_name = os.environ.get('DB_NAME', 'employeehub_db')
    constructed_mysql_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    
    # Retrieve DATABASE_URL from environment or use constructed
    DATABASE_URL = os.environ.get('DATABASE_URL') or constructed_mysql_url
    
    # Support Render's postgres:// -> postgresql:// or mysql:// -> mysql+pymysql://
    if DATABASE_URL.startswith("mysql://"):
        DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
    elif DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Fallback to local SQLite if USE_SQLITE is true
    if os.environ.get('USE_SQLITE', 'false').lower() in ('true', '1', 'yes'):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'employeehub.db')}"
    else:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-secret-fallback-key-must-override')

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
