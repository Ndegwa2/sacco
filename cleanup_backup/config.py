import os
# config.py
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance (used throughout the app)
db = SQLAlchemy()

# App configuration function
def configure_app(app):
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Ndegwa_Sacco')
    
    # Use environment variable for database URL, fallback to local SQLite for development
    database_url = os.environ.get('DATABASE_URL')
    
    # Handle Render's postgres:// URL format by converting to postgresql://
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///sacco_system.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Additional production settings
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
