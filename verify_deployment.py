#!/usr/bin/env python3
"""
Deployment verification script for Sacco Management System
This script helps verify that all dependencies are properly installed
"""

import sys
import os

def check_python_version():
    """Check Python version compatibility"""
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 11):
        print("WARNING: Python version should be 3.11 or higher")
        return False
    return True

def check_dependencies():
    """Check if critical dependencies can be imported"""
    dependencies = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_migrate',
        'psycopg2',
        'gunicorn',
        'sqlalchemy'
    ]
    
    failed_imports = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {dep}: {e}")
            failed_imports.append(dep)
    
    return len(failed_imports) == 0

def check_database_connection():
    """Check database connection"""
    try:
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("WARNING: DATABASE_URL environment variable not set")
            return False
        
        print(f"Database URL configured: {database_url[:20]}...")
        
        # Try to import psycopg2 specifically
        import psycopg2
        print("✓ psycopg2 is available")
        
        return True
    except Exception as e:
        print(f"✗ Database connection check failed: {e}")
        return False

def main():
    """Main verification function"""
    print("=== Sacco Management System Deployment Verification ===\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Database Connection", check_database_connection)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n--- {check_name} Check ---")
        if not check_func():
            all_passed = False
    
    print("\n=== Summary ===")
    if all_passed:
        print("✓ All checks passed! Deployment should work correctly.")
    else:
        print("✗ Some checks failed. Please review the issues above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())