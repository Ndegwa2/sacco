from flask import Flask
from config import db, configure_app
from server.models import Vehicle

app = Flask(__name__)
configure_app(app)
db.init_app(app)

with app.app_context():
    # Check if there are already vehicles
    existing_vehicles = Vehicle.query.all()
    if existing_vehicles:
        print(f"There are already {len(existing_vehicles)} vehicles in the database.")
    else:
        # Create a test vehicle
        test_vehicle = Vehicle(
            plate_number="KAA 123B",
            vehicle_model="Toyota Hiace",
            assigned_route="Nairobi - Mombasa",
            status="active"
        )
        
        db.session.add(test_vehicle)
        db.session.commit()
        print("Added test vehicle: KAA 123B (Toyota Hiace)")