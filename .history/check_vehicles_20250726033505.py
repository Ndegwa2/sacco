from flask import Flask
from config import db, configure_app
from server.models import Vehicle

app = Flask(__name__)
configure_app(app)
db.init_app(app)

with app.app_context():
    vehicles = Vehicle.query.all()
    print(f"Found {len(vehicles)} vehicles in the database:")
    for vehicle in vehicles:
        print(f"  ID: {vehicle.id}, Plate: {vehicle.plate_number}, Model: {vehicle.vehicle_model}, Status: {vehicle.status}")