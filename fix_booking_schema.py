#!/usr/bin/env python3
"""
Script to fix the booking schema by adding user_id column and updating date/time fields
"""

import os
import sys
from flask import Flask
from config import configure_app, db
from server.models.booking import Booking
from server.models.user import User

def fix_booking_schema():
    """Fix the booking schema by adding missing columns"""
    app = Flask(__name__)
    configure_app(app)
    db.init_app(app)
    
    with app.app_context():
        try:
            # Check if we're using SQLite
            if 'sqlite' in str(db.engine.url):
                print("🔧 Fixing SQLite database schema...")
                
                # Get the database connection
                from sqlalchemy import text
                
                # Check if user_id column exists
                result = db.session.execute(text("PRAGMA table_info(booking)"))
                columns = [row[1] for row in result.fetchall()]
                
                if 'user_id' not in columns:
                    print("➕ Adding user_id column...")
                    db.session.execute(text("ALTER TABLE booking ADD COLUMN user_id INTEGER"))
                    print("✅ user_id column added")
                else:
                    print("✅ user_id column already exists")
                
                if 'created_at' not in columns:
                    print("➕ Adding created_at column...")
                    db.session.execute(text("ALTER TABLE booking ADD COLUMN created_at DATETIME"))
                    print("✅ created_at column added")
                else:
                    print("✅ created_at column already exists")
                
                # Commit the changes
                db.session.commit()
                print("✅ Schema update completed successfully")
                
                # Show current bookings
                bookings = Booking.query.all()
                print(f"📊 Current bookings in database: {len(bookings)}")
                
                for booking in bookings:
                    print(f"  - ID: {booking.id}, Name: {booking.name}, Route: {booking.route}, User ID: {booking.user_id}")
                
            else:
                print("🔧 Non-SQLite database detected, using SQLAlchemy...")
                db.create_all()
                print("✅ Database schema updated")
                
        except Exception as e:
            print(f"❌ Error updating schema: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == "__main__":
    success = fix_booking_schema()
    if success:
        print("\n🎉 Booking schema fix completed successfully!")
    else:
        print("\n💥 Schema fix failed!")
        sys.exit(1)