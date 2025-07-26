"""
This script updates the foreign key constraint in the vehicle_health table
to reference the fleet table instead of the vehicle table.

WARNING: This will drop and recreate the vehicle_health table, so all existing
vehicle health records will be lost. Make sure to back up your data before running this.
"""

from run import app, db
from server.models.vehicle_health import VehicleHealth
from sqlalchemy import text

with app.app_context():
    # Backup existing vehicle health records if needed
    health_records = VehicleHealth.query.all()
    backup_data = []
    for record in health_records:
        backup_data.append({
            'vehicle_id': record.vehicle_id,
            'driver_id': record.driver_id,
            'check_date': record.check_date,
            'engine_condition': record.engine_condition,
            'brake_condition': record.brake_condition,
            'tire_condition': record.tire_condition,
            'lights_condition': record.lights_condition,
            'body_condition': record.body_condition,
            'fuel_level': record.fuel_level,
            'oil_level': record.oil_level,
            'coolant_level': record.coolant_level,
            'issues_noted': record.issues_noted,
            'maintenance_needed': record.maintenance_needed
        })
    
    print(f"Backed up {len(backup_data)} vehicle health records")
    
    # Drop the existing foreign key constraint and recreate it
    db.session.execute(text("ALTER TABLE vehicle_health DROP FOREIGN KEY vehicle_health_ibfk_1"))
    db.session.execute(text("ALTER TABLE vehicle_health ADD CONSTRAINT vehicle_health_ibfk_1 FOREIGN KEY (vehicle_id) REFERENCES fleet(id)"))
    db.session.commit()
    
    print("Foreign key constraint updated to reference fleet table")
    
    # Note: If you want to restore the backed up data, you would need to add code here
    # to insert the backup_data back into the vehicle_health table