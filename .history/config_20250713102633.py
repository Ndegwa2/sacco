import pymysql
pymysql.install_as_MySQLdb()
# config.py
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance (used throughout the app)
db = SQLAlchemy()

# App configuration function
def configure_app(app):
    app.config['SECRET_KEY'] = 'ee5ea2b107d77e0baf5b4cae99c4dd0dac60501886beb848f6652116711ad635'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sacco_system'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with app
    if os.environ.get('FLASK_ENV') != 'testing':
        db.init_app(app)

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
