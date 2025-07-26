from run import app, db, Vehicle, Fleet

with app.app_context():
    print("Vehicles in Vehicle table:")
    vehicles = Vehicle.query.all()
    for v in vehicles:
        print(f"ID: {v.id}, Plate: {v.plate_number}")
    
    print("\nVehicles in Fleet table:")
    fleet = Fleet.query.all()
    for f in fleet:
        print(f"ID: {f.id}, Plate: {f.plate_number}")