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
    full_name = db.Column(db.String(150), nullable=True)  # Add full_name column
    status = db.Column(db.String(50), default='active')   # Add status column
    
    def get_full_name(self):
        """Return full_name if available, otherwise username for backward compatibility"""
        return self.full_name if self.full_name else self.username
    
    def get_status(self):
        """Return status"""
        return self.status if self.status else 'active'

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
