#!/usr/bin/env python3
"""
Script to apply the capacity migration directly to the database.
This script adds the capacity column to the vehicle table.
"""

import sqlite3
import os

def apply_migration():
    # Connect to the database
    db_path = os.path.join('instance', 'sacco_system.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add capacity column to vehicle table with default value of 33
        cursor.execute("ALTER TABLE vehicle ADD COLUMN capacity INTEGER NOT NULL DEFAULT 33")
        print("Added capacity column to vehicle table")
        
        # Commit changes
        conn.commit()
        print("Migration applied successfully!")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column capacity already exists in vehicle table")
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