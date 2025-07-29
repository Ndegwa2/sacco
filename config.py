import pymysql
pymysql.install_as_MySQLdb()
import os
# config.py
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance (used throughout the app)
db = SQLAlchemy()

# App configuration function
def configure_app(app):
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Ndegwa_Sacco')
    
    # Use environment variable for database URL, fallback to local MySQL for development
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost/sacco_system'
    )
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Additional production settings
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
