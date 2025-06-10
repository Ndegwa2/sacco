from run import app
from config import db
from server.models.fleet import Fleet

with app.app_context():
    fleets = Fleet.query.all()
    for fleet in fleets:
        print(f"{fleet.plate_number}, {fleet.vehicle_model}, {fleet.assigned_route}, {fleet.status}")