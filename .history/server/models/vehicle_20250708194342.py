from config import db

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), nullable=False)
    vehicle_model = db.Column(db.String(100), nullable=False)
    assigned_route = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)