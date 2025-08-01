from config import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(100), nullable=False)
    pickup = db.Column(db.String(100), nullable=False)
    dropoff = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)  # Using String instead of Date for simplicity
    time = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')