#!/usr/bin/env python3
"""
Verification script to check that driver assignments are working properly
for the driver log dropdown functionality.
"""

import os
import sys

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

def verify_driver_log_data():
    """Verify that all data needed for driver log dropdown is available"""
    print("🔍 Verifying Driver Log Dropdown Data")
    print("="*50)
    
    # Check drivers (employees)
    drivers = User.query.filter_by(role='employee').all()
    print(f"👥 Total Drivers: {len(drivers)}")
    for driver in drivers:
        print(f"   - {driver.full_name} ({driver.username}) - Status: {driver.status}")
    
    # Check vehicles
    vehicles = Vehicle.query.filter_by(status='active').all()
    print(f"\n🚐 Total Active Vehicles: {len(vehicles)}")
    for vehicle in vehicles:
        print(f"   - {vehicle.plate_number} ({vehicle.vehicle_model}) - Status: {vehicle.status}")
    
    # Check routes
    routes = Route.query.filter_by(status='active').all()
    print(f"\n🛣️  Total Active Routes: {len(routes)}")
    for route in routes:
        print(f"   - {route.route_name}: {route.origin} → {route.destination}")
    
    # Check active assignments
    active_assignments = AssignedRoute.query.filter_by(status='active').all()
    print(f"\n🔗 Total Active Assignments: {len(active_assignments)}")
    
    # Test driver log dropdown data for each driver
    print(f"\n📋 Driver Log Dropdown Test:")
    print("-" * 50)
    
    for driver in drivers:
        print(f"\n👤 Driver: {driver.full_name}")
        
        # Get assigned routes for this driver (what should appear in dropdown)
        driver_assignments = AssignedRoute.query.filter_by(
            employee_id=driver.id,
            status='active'
        ).all()
        
        if driver_assignments:
            print(f"   ✅ Has {len(driver_assignments)} active assignment(s):")
            for assignment in driver_assignments:
                route = Route.query.get(assignment.route_id)
                vehicle = Vehicle.query.get(assignment.vehicle_id) if assignment.vehicle_id else None
                
                route_name = route.route_name if route else "Unknown Route"
                vehicle_info = f" (Vehicle: {vehicle.plate_number})" if vehicle else " (No Vehicle)"
                
                print(f"      - {route_name}{vehicle_info}")
        else:
            print(f"   ❌ No active assignments found!")
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"   - Drivers: {len(drivers)}")
    print(f"   - Active Vehicles: {len(vehicles)}")
    print(f"   - Active Routes: {len(routes)}")
    print(f"   - Active Assignments: {len(active_assignments)}")
    
    # Check if driver log should work
    drivers_with_assignments = len([d for d in drivers if AssignedRoute.query.filter_by(employee_id=d.id, status='active').first()])
    
    if drivers_with_assignments > 0:
        print(f"\n🎉 SUCCESS: {drivers_with_assignments} driver(s) have active assignments!")
        print("💡 The driver log dropdown should now work properly.")
        return True
    else:
        print(f"\n❌ ISSUE: No drivers have active assignments!")
        print("💡 The driver log dropdown may still be empty.")
        return False

def main():
    """Main function"""
    app = create_app()
    
    try:
        with app.app_context():
            success = verify_driver_log_data()
            return 0 if success else 1
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)