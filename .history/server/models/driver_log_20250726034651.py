from config import db
from datetime import datetime

class DriverLog(db.Model):
    __tablename__ = 'driver_log'
    
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    log_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    
    # Mileage information
    starting_mileage = db.Column(db.Float, nullable=False)
    ending_mileage = db.Column(db.Float, nullable=False)
    total_distance = db.Column(db.Float, nullable=False)
    
    # Earnings information
    total_earnings = db.Column(db.Float, nullable=False)
    fuel_cost = db.Column(db.Float, nullable=True)
    maintenance_cost = db.Column(db.Float, nullable=True)
    net_earnings = db.Column(db.Float, nullable=False)
    
    # Additional information
    trips_completed = db.Column(db.Integer, nullable=False, default=0)
    passengers_served = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    driver = db.relationship('User', backref='driver_logs')
    vehicle = db.relationship('Fleet', backref='vehicle_logs')
    route = db.relationship('Route', backref='route_logs')
    
    def __repr__(self):
        return f"DriverLog(id={self.id}, driver_id={self.driver_id}, vehicle_id={self.vehicle_id}, log_date={self.log_date}, total_earnings={self.total_earnings})"