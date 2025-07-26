import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Import the app and db from your application
from run import app, db

# SQL statement to add the vehicle_id column
sql = """
ALTER TABLE assigned_route 
ADD COLUMN vehicle_id INT NULL,
ADD COLUMN start_date DATE NULL,
ADD COLUMN end_date DATE NULL,
ADD COLUMN status VARCHAR(20) NULL DEFAULT 'active',
ADD COLUMN shift VARCHAR(20) NULL,
ADD COLUMN notes TEXT NULL,
ADD COLUMN created_by INT NULL,
ADD COLUMN created_at DATETIME NULL,
ADD COLUMN updated_at DATETIME NULL,
ADD CONSTRAINT fk_assigned_route_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
ADD CONSTRAINT fk_assigned_route_created_by FOREIGN KEY (created_by) REFERENCES user(id);
"""

# Apply the SQL statement
with app.app_context():
    try:
        db.session.execute(text(sql))
        db.session.commit()
        print("Successfully added vehicle_id column to assigned_route table!")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")