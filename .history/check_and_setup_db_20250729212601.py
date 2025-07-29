#!/usr/bin/env python3
"""
Script to check database schema and set up tables properly
"""
import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, text, inspect

# Load environment variables
load_dotenv()

def check_existing_tables():
    """Check what tables already exist in the database"""
    try:
        database_url = os.environ.get('DATABASE_URL')
        
        # Handle postgres:// URL format by converting to postgresql://
        if database_url and database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        engine = create_engine(database_url)
        inspector = inspect(engine)
        
        tables = inspector.get_table_names()
        print(f"📋 Existing tables in database:")
        for table in sorted(tables):
            print(f"  - {table}")
        
        return tables
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return []

def setup_flask_app_tables():
    """Set up tables using Flask app context"""
    try:
        from config import db, configure_app
        from flask import Flask
        from server.models import User, Vehicle, Route, Booking, EmployeePayment, Performance
        from server.models.user import SaccoMember
        from server.models.fleet import Fleet
        from server.models.route_assignment import AssignedRoute
        from server.models.driver_log import DriverLog
        from server.models.vehicle_health import VehicleHealth
        
        app = Flask(__name__)
        configure_app(app)
        db.init_app(app)
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ All tables created successfully using Flask-SQLAlchemy!")
            
            # Check if we can query the tables
            user_count = User.query.count()
            route_count = Route.query.count()
            print(f"📊 Current data: {user_count} users, {route_count} routes")
        
        return True
    except Exception as e:
        print(f"❌ Error setting up Flask tables: {e}")
        return False

def test_app_startup():
    """Test if the app can start properly"""
    try:
        from run import app
        
        with app.app_context():
            # Test basic database operations
            from server.models import User
            user_count = User.query.count()
            print(f"✅ App startup test successful! Found {user_count} users in database.")
        
        return True
    except Exception as e:
        print(f"❌ App startup test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking Database Schema and Setup...")
    print("=" * 50)
    
    # Step 1: Check existing tables
    print("\n1. Checking existing tables:")
    existing_tables = check_existing_tables()
    
    # Step 2: Set up tables using Flask-SQLAlchemy
    print("\n2. Setting up tables using Flask-SQLAlchemy:")
    setup_flask_app_tables()
    
    # Step 3: Test app startup
    print("\n3. Testing app startup:")
    test_app_startup()
    
    print("\n" + "=" * 50)
    print("Database setup completed!")