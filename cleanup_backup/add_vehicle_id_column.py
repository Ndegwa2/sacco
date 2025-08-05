import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Import the app and db from your application
from run import app, db

# First, check which columns already exist
check_columns_sql = """
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'assigned_route'
AND table_schema = DATABASE();
"""

# Apply the SQL statement
with app.app_context():
    try:
        # Get existing columns
        result = db.session.execute(text(check_columns_sql))
        existing_columns = [row[0] for row in result]
        print(f"Existing columns: {existing_columns}")
        
        # Build ALTER TABLE statement dynamically
        alter_statements = []
        
        # Only add columns that don't exist
        if 'vehicle_id' not in existing_columns:
            alter_statements.append("ADD COLUMN vehicle_id INT NULL")
        if 'start_date' not in existing_columns:
            alter_statements.append("ADD COLUMN start_date DATE NULL")
        if 'end_date' not in existing_columns:
            alter_statements.append("ADD COLUMN end_date DATE NULL")
        if 'status' not in existing_columns:
            alter_statements.append("ADD COLUMN status VARCHAR(20) NULL DEFAULT 'active'")
        if 'shift' not in existing_columns:
            alter_statements.append("ADD COLUMN shift VARCHAR(20) NULL")
        if 'notes' not in existing_columns:
            alter_statements.append("ADD COLUMN notes TEXT NULL")
        if 'created_by' not in existing_columns:
            alter_statements.append("ADD COLUMN created_by INT NULL")
        if 'created_at' not in existing_columns:
            alter_statements.append("ADD COLUMN created_at DATETIME NULL")
        if 'updated_at' not in existing_columns:
            alter_statements.append("ADD COLUMN updated_at DATETIME NULL")
        
        # Add foreign key constraints if needed
        # Check if foreign keys exist
        check_fk_sql = """
        SELECT constraint_name
        FROM information_schema.table_constraints
        WHERE table_name = 'assigned_route'
        AND constraint_type = 'FOREIGN KEY'
        AND table_schema = DATABASE();
        """
        result = db.session.execute(text(check_fk_sql))
        existing_constraints = [row[0] for row in result]
        
        if 'fk_assigned_route_vehicle' not in existing_constraints and 'vehicle_id' in existing_columns:
            alter_statements.append("ADD CONSTRAINT fk_assigned_route_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicle(id)")
        if 'fk_assigned_route_created_by' not in existing_constraints and 'created_by' in existing_columns:
            alter_statements.append("ADD CONSTRAINT fk_assigned_route_created_by FOREIGN KEY (created_by) REFERENCES user(id)")
        
        # If there are statements to execute, run the ALTER TABLE
        if alter_statements:
            sql = "ALTER TABLE assigned_route " + ",\n".join(alter_statements) + ";"
            print(f"Executing SQL: {sql}")
            db.session.execute(text(sql))
            db.session.commit()
            print("Successfully updated assigned_route table!")
        else:
            print("No changes needed for assigned_route table.")

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")