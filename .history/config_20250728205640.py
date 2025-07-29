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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sacco_system'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # CSRF Protection settings
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = None  # No time limit for CSRF tokens

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
