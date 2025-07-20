from config import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(100), nullable=False)
    pickup = db.Column(db.String(100), nullable=False)
    dropoff = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="pending")
    contact = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="pending")