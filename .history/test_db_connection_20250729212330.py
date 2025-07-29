#!/usr/bin/env python3
"""
Test script to verify PostgreSQL database connection
"""
import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

def test_psycopg2_connection():
    """Test direct psycopg2 connection"""
    try:
        database_url = os.environ.get('DATABASE_URL')
        print(f"Testing connection to: {database_url[:50]}...")
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Direct psycopg2 connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Direct psycopg2 connection failed: {e}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        database_url = os.environ.get('DATABASE_URL')
        
        # Handle postgres:// URL format by converting to postgresql://
        if database_url and database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print(f"✅ SQLAlchemy connection successful!")
            print(f"Connected to database: {db_name}")
        
        return True
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False

def test_flask_app_connection():
    """Test Flask app database connection"""
    try:
        from config import db, configure_app
        from flask import Flask
        
        app = Flask(__name__)
        configure_app(app)
        db.init_app(app)
        
        with app.app_context():
            # Test the connection
            result = db.session.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print(f"✅ Flask app database connection successful!")
            print(f"Connected to database: {db_name}")
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ Flask app database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing PostgreSQL Database Connection...")
    print("=" * 50)
    
    # Test 1: Direct psycopg2 connection
    print("\n1. Testing direct psycopg2 connection:")
    test_psycopg2_connection()
    
    # Test 2: SQLAlchemy connection
    print("\n2. Testing SQLAlchemy connection:")
    test_sqlalchemy_connection()
    
    # Test 3: Flask app connection
    print("\n3. Testing Flask app database connection:")
    test_flask_app_connection()
    
    print("\n" + "=" * 50)
    print("Database connection tests completed!")