from config import db

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    stops = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False)