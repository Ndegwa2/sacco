# config.py
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance (used throughout the app)
db = SQLAlchemy()

# App configuration function
def configure_app(app):
    app.config['SECRET_KEY'] = 'ee5ea2b107d77e0baf5b4cae99c4dd0dac60501886beb848f6652116711ad635'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sacco_system.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with app
    db.init_app(app)
