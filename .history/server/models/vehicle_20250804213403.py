from config import db
from datetime import datetime

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), nullable=False, unique=True)
    vehicle_model = db.Column(db.String(100), nullable=False)
    assigned_route = db.Column(db.String(100), nullable=True)  # Made nullable for flexibility
    status = db.Column(db.String(50), nullable=False, default='active')
    
    # Additional fields for better vehicle management
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"Vehicle(id={self.id}, plate_number='{self.plate_number}', model='{self.vehicle_model}', status='{self.status}')"