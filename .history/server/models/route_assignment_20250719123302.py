from config import db
from datetime import date

class RouteAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    assigned_date = db.Column(db.Date, default=date.today)

    employee = db.relationship('User', backref='route_assignments')
    route = db.relationship('Route', backref='assigned_employees')