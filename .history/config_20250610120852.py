# config.py
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance (used throughout your app)
db = SQLAlchemy()

# App configuration function
def configure_app(app):
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a strong secret in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sacco_system.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with app
    db.init_app(app)
