from config import db
from datetime import datetime

class AssignedRoute(db.Model):
    __tablename__ = 'assigned_route'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    route_id = db.Column(db.Integer, nullable=False)
    date_assigned = db.Column(db.DateTime, default=datetime.utcnow)