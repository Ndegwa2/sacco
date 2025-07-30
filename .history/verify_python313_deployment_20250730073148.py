#!/usr/bin/env python3
"""
Verification script for Python 3.13 deployment compatibility
Checks if the current environment can handle the updated dependencies
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """Check if Python version matches deployment requirements"""
    print("=== Python Version Check ===")
    current_version = sys.version_info
    print(f"Current Python version: {current_version.major}.{current_version.minor}.{current_version.micro}")
    
    # Read runtime.txt to get expected version
    runtime_file = Path("runtime.txt")
    if runtime_file.exists():
        with open(runtime_file, 'r') as f:
            expected_version = f.read().strip().replace('python-', '')
        print(f"Expected version (runtime.txt): {expected_version}")
        
        # Extract major.minor from expected version
        expected_parts = expected_version.split('.')
        expected_major_minor = f"{expected_parts[0]}.{expected_parts[1]}"
        current_major_minor = f"{current_version.major}.{current_version.minor}"
        
        if current_major_minor == expected_major_minor:
            print("✅ Python version matches deployment configuration")
            return True
        else:
            print(f"⚠️  Python version mismatch. Current: {current_major_minor}, Expected: {expected_major_minor}")
            return False
    else:
        print("❌ runtime.txt not found")
        return False

def check_psycopg2_compatibility():
    """Check if psycopg2 can be imported successfully"""
    print("\n=== psycopg2 Compatibility Check ===")
    
    try:
        import psycopg2
        print(f"✅ psycopg2 imported successfully")
        print(f"   Version: {psycopg2.__version__}")
        
        # Test basic functionality
        try:
            # This should work even without a database connection
            from psycopg2 import sql
            print("✅ psycopg2.sql module accessible")
            return True
        except Exception as e:
            print(f"⚠️  psycopg2 imported but has issues: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import psycopg2: {e}")
        print("   This indicates a compatibility issue with the current Python version")
        return False

def check_alternative_psycopg():
    """Check if psycopg3 is available as an alternative"""
    print("\n=== psycopg3 Alternative Check ===")
    
    try:
        import psycopg
        print(f"✅ psycopg3 is available")
        print(f"   Version: {psycopg.__version__}")
        return True
    except ImportError:
        print("ℹ️  psycopg3 not installed (this is optional)")
        return False

def check_requirements_file():
    """Check requirements.txt for psycopg dependencies"""
    print("\n=== Requirements File Check ===")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    with open(requirements_file, 'r') as f:
        content = f.read()
    
    psycopg2_found = False
    psycopg3_found = False
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('psycopg2-binary'):
            print(f"✅ Found psycopg2-binary: {line}")
            psycopg2_found = True
        elif line.startswith('psycopg[') and not line.startswith('#'):
            print(f"✅ Found psycopg3: {line}")
            psycopg3_found = True
        elif 'psycopg[' in line and line.startswith('#'):
            print(f"ℹ️  Found commented psycopg3 option: {line}")
    
    if psycopg2_found:
        print("✅ psycopg2-binary dependency configured")
        return True
    elif psycopg3_found:
        print("✅ psycopg3 dependency configured")
        return True
    else:
        print("❌ No PostgreSQL adapter found in requirements.txt")
        return False

def check_flask_sqlalchemy():
    """Check if Flask-SQLAlchemy works with the current setup"""
    print("\n=== Flask-SQLAlchemy Compatibility Check ===")
    
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        # Create a minimal Flask app to test SQLAlchemy
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        with app.app_context():
            db = SQLAlchemy(app)
            print("✅ Flask-SQLAlchemy initialized successfully")
            return True
            
    except Exception as e:
        print(f"❌ Flask-SQLAlchemy compatibility issue: {e}")
        return False

def suggest_fixes():
    """Provide suggestions for fixing compatibility issues"""
    print("\n=== Suggested Fixes ===")
    
    current_version = sys.version_info
    if current_version.major == 3 and current_version.minor >= 13:
        print("For Python 3.13+ compatibility:")
        print("1. Use psycopg2-binary==2.9.10 (latest version)")
        print("2. If psycopg2 fails, switch to psycopg3:")
        print("   - Comment out: psycopg2-binary==2.9.10")
        print("   - Uncomment: psycopg[binary]==3.1.18")
        print("3. Ensure runtime.txt specifies python-3.13.0")
        print("4. Update render.yaml pythonVersion to '3.13.0'")
    else:
        print("For older Python versions:")
        print("1. Consider upgrading to Python 3.13 for better compatibility")
        print("2. Use psycopg2-binary==2.9.9 for Python 3.11")

def main():
    """Run all compatibility checks"""
    print("Python 3.13 Deployment Compatibility Checker")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_requirements_file(),
        check_psycopg2_compatibility(),
        check_alternative_psycopg(),
        check_flask_sqlalchemy()
    ]
    
    passed_checks = sum(checks)
    total_checks = len(checks)
    
    print(f"\n=== Summary ===")
    print(f"Passed: {passed_checks}/{total_checks} checks")
    
    if passed_checks == total_checks:
        print("🎉 All checks passed! Your configuration should work for deployment.")
    elif passed_checks >= 3:
        print("⚠️  Most checks passed. Minor issues may need attention.")
    else:
        print("❌ Several issues detected. Review the suggestions below.")
    
    suggest_fixes()

if __name__ == "__main__":
    main()