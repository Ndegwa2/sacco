from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import db

# db = SQLAlchemy()  # local definition here (remove from config.py)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='passenger')  # admin, passenger
    
    @property
    def full_name(self):
        """Return username as full_name for backward compatibility"""
        return self.username
    
    @property
    def status(self):
        """Return 'active' as default status for backward compatibility"""
        return 'active'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SaccoMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    id_number = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(50))
    shareholding = db.Column(db.Float)
