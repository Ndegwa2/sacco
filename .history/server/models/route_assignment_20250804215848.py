from config import db
from datetime import datetime

class AssignedRoute(db.Model):
    __tablename__ = 'assigned_route'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    date_assigned = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    end_date = db.Column(db.Date, nullable=True)
    
    # Assignment status: 'active', 'completed', 'cancelled'
    status = db.Column(db.String(20), nullable=False, default='active')
    
    # Additional metadata
    shift = db.Column(db.String(20), nullable=True)  # 'morning', 'afternoon', 'evening'
    notes = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = db.relationship('User', foreign_keys=[employee_id], backref='assignments')
    route = db.relationship('Route', backref='assigned_routes')
    vehicle = db.relationship('Vehicle', backref='driver_route_assignments')
    admin = db.relationship('User', foreign_keys=[created_by], backref='created_assignments')
    
    def __repr__(self):
        return f"AssignedRoute(id={self.id}, employee_id={self.employee_id}, route_id={self.route_id}, vehicle_id={self.vehicle_id}, status={self.status})"