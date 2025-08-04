"""
Migration script to consolidate Fleet data into Vehicle model.
This script will:
1. Copy all data from Fleet table to Vehicle table
2. Update foreign key references in related tables
3. Verify data integrity after migration
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from run import app, db
from server.models.fleet import Fleet
from server.models.vehicle import Vehicle
from server.models.driver_log import DriverLog
from server.models.vehicle_health import VehicleHealth
from sqlalchemy import text

def migrate_fleet_to_vehicle():
    """Migrate all Fleet data to Vehicle model"""
    with app.app_context():
        try:
            print("Starting Fleet to Vehicle migration...")
            
            # Step 1: Get all Fleet records
            fleet_records = Fleet.query.all()
            print(f"Found {len(fleet_records)} Fleet records to migrate")
            
            # Step 2: Copy Fleet data to Vehicle table
            migrated_count = 0
            for fleet_record in fleet_records:
                # Check if vehicle already exists
                existing_vehicle = Vehicle.query.filter_by(plate_number=fleet_record.plate_number).first()
                
                if not existing_vehicle:
                    # Create new Vehicle record
                    new_vehicle = Vehicle(
                        plate_number=fleet_record.plate_number,
                        vehicle_model=fleet_record.vehicle_model,
                        assigned_route=fleet_record.assigned_route,
                        status=fleet_record.status,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(new_vehicle)
                    db.session.flush()  # Get the ID without committing
                    
                    # Update DriverLog records to reference the new Vehicle
                    driver_logs = DriverLog.query.filter_by(vehicle_id=fleet_record.id).all()
                    for log in driver_logs:
                        log.vehicle_id = new_vehicle.id
                    
                    migrated_count += 1
                    print(f"Migrated: {fleet_record.plate_number} -> Vehicle ID: {new_vehicle.id}")
                else:
                    print(f"Vehicle with plate {fleet_record.plate_number} already exists, skipping...")
            
            # Step 3: Commit all changes
            db.session.commit()
            print(f"Successfully migrated {migrated_count} vehicles")
            
            # Step 4: Verify migration
            verify_migration()
            
        except Exception as e:
            print(f"Error during migration: {e}")
            db.session.rollback()
            raise

def verify_migration():
    """Verify that the migration was successful"""
    print("\nVerifying migration...")
    
    # Check Vehicle table
    vehicle_count = Vehicle.query.count()
    print(f"Total vehicles in Vehicle table: {vehicle_count}")
    
    # Check DriverLog references
    driver_logs = DriverLog.query.all()
    invalid_references = 0
    for log in driver_logs:
        vehicle = Vehicle.query.get(log.vehicle_id)
        if not vehicle:
            invalid_references += 1
    
    if invalid_references == 0:
        print("✅ All DriverLog records have valid Vehicle references")
    else:
        print(f"❌ Found {invalid_references} invalid Vehicle references in DriverLog")
    
    # Check VehicleHealth references
    health_checks = VehicleHealth.query.all()
    invalid_health_references = 0
    for check in health_checks:
        vehicle = Vehicle.query.get(check.vehicle_id)
        if not vehicle:
            invalid_health_references += 1
    
    if invalid_health_references == 0:
        print("✅ All VehicleHealth records have valid Vehicle references")
    else:
        print(f"❌ Found {invalid_health_references} invalid Vehicle references in VehicleHealth")

def cleanup_fleet_table():
    """
    Optional: Remove Fleet table after successful migration.
    WARNING: This is irreversible!
    """
    response = input("\nDo you want to remove the Fleet table? (yes/no): ")
    if response.lower() == 'yes':
        try:
            with app.app_context():
                # Drop the Fleet table
                db.session.execute(text("DROP TABLE IF EXISTS fleet"))
                db.session.commit()
                print("✅ Fleet table removed successfully")
        except Exception as e:
            print(f"❌ Error removing Fleet table: {e}")
    else:
        print("Fleet table preserved")

if __name__ == "__main__":
    print("Fleet to Vehicle Migration Script")
    print("=" * 40)
    
    # Run migration
    migrate_fleet_to_vehicle()
    
    # Ask if user wants to cleanup
    print("\nMigration completed successfully!")
    cleanup_fleet_table()