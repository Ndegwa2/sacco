#!/usr/bin/env python3
"""
Simple script to view current users in the database
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from run import app, db
from server.models.user import User

def view_current_users():
    """Display all current users in the database"""
    with app.app_context():
        try:
            users = User.query.all()
            print(f"\n📋 Current Users in Database ({len(users)} total):")
            print("=" * 80)
            print(f"{'ID':<4} {'Username':<15} {'Full Name':<20} {'Email':<25} {'Role':<10} {'Status':<8}")
            print("-" * 80)
            
            for user in users:
                print(f"{user.id:<4} {user.username:<15} {user.get_full_name():<20} {user.email or 'N/A':<25} {user.role:<10} {user.get_status():<8}")
            
            print(f"\n📊 Summary:")
            print(f"   Total users: {len(users)}")
            print(f"   Admin users: {len([u for u in users if u.role == 'admin'])}")
            print(f"   Employee users: {len([u for u in users if u.role == 'employee'])}")
            print(f"   Passenger users: {len([u for u in users if u.role == 'passenger'])}")
            
            return users
        except Exception as e:
            print(f"❌ Error viewing users: {e}")
            return []

if __name__ == "__main__":
    print("🏦 Sacco Management System - Current Users")
    print("=" * 50)
    view_current_users()