from run import app, db, Vehicle, Fleet

with app.app_context():
    # Get all vehicles from Fleet table
    fleet_vehicles = Fleet.query.all()
    
    # Copy them to Vehicle table
    for fleet_vehicle in fleet_vehicles:
        # Check if vehicle already exists in Vehicle table
        existing_vehicle = Vehicle.query.filter_by(id=fleet_vehicle.id).first()
        if not existing_vehicle:
            new_vehicle = Vehicle(
                id=fleet_vehicle.id,
                plate_number=fleet_vehicle.plate_number,
                vehicle_model=fleet_vehicle.vehicle_model,
                assigned_route=fleet_vehicle.assigned_route or "Unknown",
                status=fleet_vehicle.status
            )
            db.session.add(new_vehicle)
    
    # Commit changes
    db.session.commit()
    
    print("Vehicles copied from Fleet to Vehicle table")
    
    # Verify
    print("\nVehicles in Vehicle table after copy:")
    vehicles = Vehicle.query.all()
    for v in vehicles:
        print(f"ID: {v.id}, Plate: {v.plate_number}")