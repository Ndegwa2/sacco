#!/usr/bin/env python3
"""
Script to assign drivers to routes with vehicles.
This script will:
1. Create three driver users (if they don't exist)
2. Ensure there are vehicles and routes in the database
3. Assign each driver to a specific route with a vehicle
4. Use the AssignedRoute model to create proper route assignments
5. Fix the driver log dropdown issue by providing active route assignments
"""

import os
import sys
from datetime import datetime, date, timedelta

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from config import db, configure_app
from server.models.user import User
from server.models.vehicle import Vehicle
from server.models.route import Route
from server.models.route_assignment import AssignedRoute

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    configure_app(app)
    db.init_app(app)
    return app

def create_driver_users(app):
    """Create three driver users if they don't exist"""
    with app.app_context():
        drivers_data = [
            {
                'username': 'driver001',
                'email': 'driver001@naismart.com',
                'full_name': 'John Kamau',
                'password': 'driver123'
            },
            {
                'username': 'driver002',
                'email': 'driver002@naismart.com',
                'full_name': 'Mary Wanjiku',
                'password': 'driver123'
            },
            {
                'username': 'driver003',
                'email': 'driver003@naismart.com',
                'full_name': 'Peter Otieno',
                'password': 'driver123'
            }
        ]
        
        created_drivers = []
        
        for driver_data in drivers_data:
            # Check if driver already exists
            existing_driver = User.query.filter_by(username=driver_data['username']).first()
            
            if not existing_driver:
                # Create new driver
                new_driver = User(
                    username=driver_data['username'],
                    email=driver_data['email'],
                    full_name=driver_data['full_name'],
                    role='employee',
                    status='active'
                )
                new_driver.set_password(driver_data['password'])
                
                db.session.add(new_driver)
                created_drivers.append(new_driver)
                print(f"✅ Created driver: {driver_data['full_name']} ({driver_data['username']})")
            else:
                # Update role to employee if it's not already
                if existing_driver.role != 'employee':
                    existing_driver.role = 'employee'
                    existing_driver.status = 'active'
                    db.session.add(existing_driver)
                    print(f"✅ Updated existing user to driver: {existing_driver.full_name} ({existing_driver.username})")
                else:
                    print(f"ℹ️  Driver already exists: {existing_driver.full_name} ({existing_driver.username})")
                created_drivers.append(existing_driver)
        
        db.session.commit()
        return created_drivers

def create_vehicles(app):
    """Create vehicles if they don't exist"""
    with app.app_context():
        vehicles_data = [
            {
                'plate_number': 'KCA 001A',
                'vehicle_model': 'Toyota Hiace',
                'status': 'active'
            },
            {
                'plate_number': 'KCB 002B',
                'vehicle_model': 'Nissan Matatu',
                'status': 'active'
            },
            {
                'plate_number': 'KCC 003C',
                'vehicle_model': 'Isuzu Forward',
                'status': 'active'
            }
        ]
        
        created_vehicles = []
        
        for vehicle_data in vehicles_data:
            # Check if vehicle already exists
            existing_vehicle = Vehicle.query.filter_by(plate_number=vehicle_data['plate_number']).first()
            
            if not existing_vehicle:
                # Create new vehicle
                new_vehicle = Vehicle(
                    plate_number=vehicle_data['plate_number'],
                    vehicle_model=vehicle_data['vehicle_model'],
                    status=vehicle_data['status']
                )
                
                db.session.add(new_vehicle)
                created_vehicles.append(new_vehicle)
                print(f"✅ Created vehicle: {vehicle_data['plate_number']} ({vehicle_data['vehicle_model']})")
            else:
                print(f"ℹ️  Vehicle already exists: {existing_vehicle.plate_number} ({existing_vehicle.vehicle_model})")
                created_vehicles.append(existing_vehicle)
        
        db.session.commit()
        return created_vehicles

def create_routes(app):
    """Create routes if they don't exist"""
    with app.app_context():
        routes_data = [
            {
                'route_name': 'Nairobi-Thika Route',
                'origin': 'Nairobi CBD',
                'destination': 'Thika Town',
                'stops': 'Kasarani, Ruiru, Juja, Thika Road',
                'status': 'active'
            },
            {
                'route_name': 'Nairobi-Kiambu Route',
                'origin': 'Nairobi CBD',
                'destination': 'Kiambu Town',
                'stops': 'Westlands, Banana Hill, Limuru Road, Kiambu',
                'status': 'active'
            },
            {
                'route_name': 'Nairobi-Machakos Route',
                'origin': 'Nairobi CBD',
                'destination': 'Machakos Town',
                'stops': 'Imara Daima, Kitengela, Athi River, Machakos',
                'status': 'active'
            }
        ]
        
        created_routes = []
        
        for route_data in routes_data:
            # Check if route already exists
            existing_route = Route.query.filter_by(route_name=route_data['route_name']).first()
            
            if not existing_route:
                # Create new route
                new_route = Route(
                    route_name=route_data['route_name'],
                    origin=route_data['origin'],
                    destination=route_data['destination'],
                    stops=route_data['stops'],
                    status=route_data['status']
                )
                
                db.session.add(new_route)
                created_routes.append(new_route)
                print(f"✅ Created route: {route_data['route_name']}")
            else:
                print(f"ℹ️  Route already exists: {existing_route.route_name}")
                created_routes.append(existing_route)
        
        db.session.commit()
        return created_routes

def assign_drivers_to_routes(app, drivers, vehicles, routes):
    """Assign each driver to a specific route with a vehicle"""
    with app.app_context():
        assignments_created = []
        
        # Create assignments for each driver
        for i, driver in enumerate(drivers):
            if i < len(vehicles) and i < len(routes):
                vehicle = vehicles[i]
                route = routes[i]
                
                # Check if assignment already exists
                existing_assignment = AssignedRoute.query.filter_by(
                    employee_id=driver.id,
                    route_id=route.id,
                    status='active'
                ).first()
                
                if not existing_assignment:
                    # Create new assignment
                    new_assignment = AssignedRoute(
                        employee_id=driver.id,
                        route_id=route.id,
                        vehicle_id=vehicle.id,
                        start_date=date.today(),
                        end_date=None,  # Open-ended assignment
                        status='active',
                        shift='morning',
                        notes=f'Initial assignment for {driver.full_name}',
                        created_by=1  # Assuming admin user ID is 1
                    )
                    
                    db.session.add(new_assignment)
                    assignments_created.append(new_assignment)
                    
                    print(f"✅ Assigned {driver.full_name} to {route.route_name} with vehicle {vehicle.plate_number}")
                else:
                    print(f"ℹ️  Assignment already exists: {driver.full_name} -> {route.route_name}")
                    assignments_created.append(existing_assignment)
        
        db.session.commit()
        return assignments_created

def verify_assignments(app):
    """Verify that assignments were created successfully"""
    with app.app_context():
        print("\n" + "="*60)
        print("VERIFICATION: Current Active Route Assignments")
        print("="*60)
        
        active_assignments = AssignedRoute.query.filter_by(status='active').all()
        
        if not active_assignments:
            print("❌ No active assignments found!")
            return False
        
        for assignment in active_assignments:
            driver = User.query.get(assignment.employee_id)
            route = Route.query.get(assignment.route_id)
            vehicle = Vehicle.query.get(assignment.vehicle_id) if assignment.vehicle_id else None
            
            driver_name = driver.full_name if driver else "Unknown Driver"
            route_name = route.route_name if route else "Unknown Route"
            vehicle_plate = vehicle.plate_number if vehicle else "No Vehicle"
            
            print(f"👤 {driver_name} -> 🛣️  {route_name} -> 🚐 {vehicle_plate}")
        
        print(f"\nTotal active assignments: {len(active_assignments)}")
        return True

def main():
    """Main function to run the script"""
    print("🚀 Starting Driver-Route Assignment Script")
    print("="*50)
    
    # Create Flask app
    app = create_app()
    
    try:
        # Create database tables
        with app.app_context():
            db.create_all()
            print("✅ Database tables created/verified")
        
        # Step 1: Create driver users
        print("\n📝 Step 1: Creating driver users...")
        drivers = create_driver_users(app)
        
        # Step 2: Create vehicles
        print("\n🚐 Step 2: Creating vehicles...")
        vehicles = create_vehicles(app)
        
        # Step 3: Create routes
        print("\n🛣️  Step 3: Creating routes...")
        routes = create_routes(app)
        
        # Step 4: Assign drivers to routes with vehicles
        print("\n🔗 Step 4: Assigning drivers to routes...")
        assignments = assign_drivers_to_routes(app, drivers, vehicles, routes)
        
        # Step 5: Verify assignments
        print("\n🔍 Step 5: Verifying assignments...")
        success = verify_assignments(app)
        
        if success:
            print("\n🎉 SUCCESS: All drivers have been assigned to routes with vehicles!")
            print("💡 The driver log dropdown should now work properly.")
        else:
            print("\n❌ FAILED: Some assignments may not have been created properly.")
            return 1
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)