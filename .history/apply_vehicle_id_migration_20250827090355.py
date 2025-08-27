#!/usr/bin/env python3
"""
Script to apply the vehicle_id migration directly to the database.
This script adds the vehicle_id column to the booking table.
"""

import sqlite3
import os

def apply_migration():
    # Connect to the database
    db_path = os.path.join('instance', 'sacco_system.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add vehicle_id column to booking table
        cursor.execute("ALTER TABLE booking ADD COLUMN vehicle_id INTEGER")
        print("Added vehicle_id column to booking table")
        
        # Add foreign key constraint (SQLite doesn't enforce FK by default, but we'll add the reference)
        # Note: SQLite doesn't support adding foreign key constraints to existing tables directly
        # The constraint will be enforced by the application logic
        
        # Commit changes
        conn.commit()
        print("Migration applied successfully!")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column vehicle_id already exists in booking table")
        else:
            print(f"Error applying migration: {e}")
            conn.rollback()
    except Exception as e:
        print(f"Error applying migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    apply_migration()