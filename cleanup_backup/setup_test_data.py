"""
Setup test data for the Sacco Management System
Creates admin user, test vehicles, and routes for testing vehicle-route assignment functionality
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from run import app, db
from server.models.user import User
from server.models.vehicle import Vehicle
from server.models.route import Route

def setup_test_data():
    """Create test data for the system"""
    with app.app_context():
        try:
            print("Setting up test data...")
            
            # Create admin user
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@naismart.com',
                    role='admin',
                    full_name='System Administrator'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                print("✅ Created admin user (username: admin, password: admin123)")
            else:
                print("ℹ️  Admin user already exists")
            
            # Create test vehicles
            vehicles_data = [
                {'plate_number': 'KDA 123A', 'vehicle_model': 'Nissan Caravan', 'status': 'active'},
                {'plate_number': 'KDB 456B', 'vehicle_model': 'Toyota Hiace', 'status': 'active'},
                {'plate_number': 'KDC 789C', 'vehicle_model': 'Isuzu NQR', 'status': 'active'},
                {'plate_number': 'KDD 012D', 'vehicle_model': 'Mitsubishi Rosa', 'status': 'inactive'},
                {'plate_number': 'KDE 345E', 'vehicle_model': 'Nissan Matatu', 'status': 'active'},
            ]
            
            vehicles_created = 0
            for vehicle_data in vehicles_data:
                existing_vehicle = Vehicle.query.filter_by(plate_number=vehicle_data['plate_number']).first()
                if not existing_vehicle:
                    vehicle = Vehicle(
                        plate_number=vehicle_data['plate_number'],
                        vehicle_model=vehicle_data['vehicle_model'],
                        status=vehicle_data['status'],
                        assigned_route=None,  # Will be assigned through the new interface
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(vehicle)
                    vehicles_created += 1
            
            print(f"✅ Created {vehicles_created} test vehicles")
            
            # Create test routes
            routes_data = [
                {
                    'route_name': 'CBD - Rongai',
                    'origin': 'Nairobi CBD',
                    'destination': 'Rongai',
                    'stops': 'Kencom, Koja, Karen, Rongai',
                    'status': 'active'
                },
                {
                    'route_name': 'Westlands - Kikuyu',
                    'origin': 'Westlands',
                    'destination': 'Kikuyu',
                    'stops': 'Westlands, Kangemi, Kinoo, Kikuyu',
                    'status': 'active'
                },
                {
                    'route_name': 'Town - Kasarani',
                    'origin': 'Nairobi CBD',
                    'destination': 'Kasarani',
                    'stops': 'Kencom, Thika Road, Kasarani',
                    'status': 'active'
                },
                {
                    'route_name': 'Machakos - Nairobi',
                    'origin': 'Machakos',
                    'destination': 'Nairobi CBD',
                    'stops': 'Machakos, Mlolongo, Imara Daima, CBD',
                    'status': 'active'
                },
                {
                    'route_name': 'Ngong - Town',
                    'origin': 'Ngong',
                    'destination': 'Nairobi CBD',
                    'stops': 'Ngong, Karen, Langata, CBD',
                    'status': 'inactive'
                }
            ]
            
            routes_created = 0
            for route_data in routes_data:
                existing_route = Route.query.filter_by(route_name=route_data['route_name']).first()
                if not existing_route:
                    route = Route(
                        route_name=route_data['route_name'],
                        origin=route_data['origin'],
                        destination=route_data['destination'],
                        stops=route_data['stops'],
                        status=route_data['status']
                    )
                    db.session.add(route)
                    routes_created += 1
            
            print(f"✅ Created {routes_created} test routes")
            
            # Create a test employee user
            employee = User.query.filter_by(username='driver1').first()
            if not employee:
                employee = User(
                    username='driver1',
                    email='driver1@naismart.com',
                    role='employee',
                    full_name='John Kamau'
                )
                employee.set_password('driver123')
                db.session.add(employee)
                print("✅ Created test driver (username: driver1, password: driver123)")
            else:
                print("ℹ️  Test driver already exists")
            
            # Commit all changes
            db.session.commit()
            
            print("\n🎉 Test data setup completed successfully!")
            print("\n📋 Login Credentials:")
            print("   Admin: username=admin, password=admin123")
            print("   Driver: username=driver1, password=driver123")
            print("\n🚗 Test Vehicles Created:")
            for vehicle_data in vehicles_data:
                print(f"   - {vehicle_data['plate_number']} ({vehicle_data['vehicle_model']}) - {vehicle_data['status']}")
            print("\n🛣️  Test Routes Created:")
            for route_data in routes_data:
                print(f"   - {route_data['route_name']} ({route_data['origin']} → {route_data['destination']}) - {route_data['status']}")
            
            print("\n🔗 Access the system:")
            print("   - Homepage: http://127.0.0.1:5000")
            print("   - Admin Panel: http://127.0.0.1:5000/login (login as admin)")
            print("   - Vehicle-Route Assignment: http://127.0.0.1:5000/admin/vehicle-route-assignment")
            
        except Exception as e:
            print(f"❌ Error setting up test data: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    setup_test_data()