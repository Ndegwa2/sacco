from config import db
from datetime import datetime

class VehicleRouteAssignment(db.Model):
    """
    Model for direct vehicle-to-route assignments without requiring a driver.
    This allows admins to assign vehicles to routes independently of driver assignments.
    """
    __tablename__ = 'vehicle_route_assignment'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    
    # Assignment details
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    end_date = db.Column(db.Date, nullable=True)
    
    # Assignment status: 'active', 'completed', 'cancelled'
    status = db.Column(db.String(20), nullable=False, default='active')
    
    # Additional metadata
    priority = db.Column(db.String(20), nullable=True, default='normal')  # 'high', 'normal', 'low'
    notes = db.Column(db.Text, nullable=True)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vehicle = db.relationship('Vehicle', backref='direct_route_assignments')
    route = db.relationship('Route', backref='direct_vehicle_assignments')
    admin = db.relationship('User', foreign_keys=[assigned_by], backref='created_vehicle_route_assignments')
    
    def __repr__(self):
        return f"VehicleRouteAssignment(id={self.id}, vehicle_id={self.vehicle_id}, route_id={self.route_id}, status={self.status})"
    
    @property
    def is_active(self):
        """Check if the assignment is currently active"""
        return self.status == 'active'
    
    @property
    def duration_days(self):
        """Calculate the duration of the assignment in days"""
        if self.end_date:
            return (self.end_date - self.start_date).days
        else:
            return (datetime.now().date() - self.start_date).days