from config import db
from datetime import datetime

class VehicleHealth(db.Model):
    __tablename__ = 'vehicle_health'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    check_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Vehicle condition ratings (1-5 scale)
    engine_condition = db.Column(db.Integer, nullable=False)
    brake_condition = db.Column(db.Integer, nullable=False)
    tire_condition = db.Column(db.Integer, nullable=False)
    lights_condition = db.Column(db.Integer, nullable=False)
    body_condition = db.Column(db.Integer, nullable=False)
    
    # Fluid levels (1-5 scale)
    fuel_level = db.Column(db.Integer, nullable=False)
    oil_level = db.Column(db.Integer, nullable=False)
    coolant_level = db.Column(db.Integer, nullable=False)
    
    # Additional information
    issues_noted = db.Column(db.Text)
    maintenance_needed = db.Column(db.Boolean, default=False)
    
    # Relationships
    vehicle = db.relationship('Vehicle', backref='health_checks')
    driver = db.relationship('User', backref='vehicle_health_checks')
    
    def __repr__(self):
        return f"VehicleHealth(id={self.id}, vehicle_id={self.vehicle_id}, driver_id={self.driver_id}, check_date={self.check_date})"