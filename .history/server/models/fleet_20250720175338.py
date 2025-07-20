from config import db
from datetime import datetime

class Fleet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), nullable=False, unique=True)
    vehicle_model = db.Column(db.String(100), nullable=False)
    assigned_route = db.Column(db.String(100))
    status = db.Column(db.String(50), default='active')

class EmployeePayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

    # Relationships
    employee = db.relationship('User', backref='payments')