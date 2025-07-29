#!/usr/bin/env python3
"""
Script to fix password hashes that are incompatible with Python 3.8
This will reset all user passwords to a default password with compatible hashing
"""

import os
import sys
from flask import Flask
from werkzeug.security import generate_password_hash

# Add the project directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config import db, configure_app
from server.models.user import User

def fix_password_hashes():
    """Fix incompatible password hashes by resetting to default password"""
    
    # Create Flask app
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'Ndegwa_Sacco')
    
    # Configure and initialize extensions
    configure_app(app)
    db.init_app(app)
    
    with app.app_context():
        try:
            # Get all users
            users = User.query.all()
            print(f"Found {len(users)} users to update")
            
            # Default password for all users
            default_password = "password123"
            
            for user in users:
                try:
                    # Generate new compatible password hash
                    new_hash = generate_password_hash(default_password, method='pbkdf2:sha256')
                    user.password_hash = new_hash
                    print(f"Updated password hash for user: {user.username}")
                except Exception as e:
                    print(f"Error updating user {user.username}: {e}")
            
            # Commit all changes
            db.session.commit()
            print("✅ All password hashes updated successfully!")
            print(f"🔑 Default password for all users is now: {default_password}")
            print("⚠️  Please ask users to change their passwords after login")
            
        except Exception as e:
            print(f"❌ Error fixing password hashes: {e}")
            db.session.rollback()

if __name__ == "__main__":
    fix_password_hashes()