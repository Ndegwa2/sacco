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
        # Vehicle data
        vehicles = [
            {"plate": "KAA 123B", "model": "Toyota Hiace", "route": "Nairobi - Mombasa", "status": "active"},
            {"plate": "KBB 456C", "model": "Nissan Urvan", "route": "Nairobi - Nakuru", "status": "active"},
            {"plate": "KCC 789D", "model": "Toyota Coaster", "route": "Nairobi - Kisumu", "status": "active"},
            {"plate": "KDD 012E", "model": "Isuzu NQR", "route": "Nairobi - Eldoret", "status": "active"},
            {"plate": "KEE 345F", "model": "Mitsubishi Rosa", "route": "Nairobi - Nyeri", "status": "active"},
            {"plate": "KFF 678G", "model": "Hino Liesse", "route": "Nairobi - Machakos", "status": "active"},
            {"plate": "KGG 901H", "model": "Toyota Hiace", "route": "Nairobi - Thika", "status": "active"},
            {"plate": "KHH 234I", "model": "Nissan Civilian", "route": "Nairobi - Kitui", "status": "active"},
            {"plate": "KII 567J", "model": "Isuzu MV", "route": "Nairobi - Naivasha", "status": "active"},
            {"plate": "KJJ 890K", "model": "Toyota Coaster", "route": "Nairobi - Kajiado", "status": "active"}
        ]
        
        # Add all vehicles
        for v in vehicles:
            vehicle = Vehicle(
                plate_number=v["plate"],
                vehicle_model=v["model"],
                assigned_route=v["route"],
                status=v["status"]
            )
            db.session.add(vehicle)
        
        db.session.commit()
        print(f"Added {len(vehicles)} test vehicles to the database.")