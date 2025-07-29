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
