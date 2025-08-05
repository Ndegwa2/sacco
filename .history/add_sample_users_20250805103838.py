#!/usr/bin/env python3
"""
Script to add sample users with proper name-based usernames
This demonstrates the new approach of using actual names as login credentials
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from run import app, db
from server.models.user import User

def add_sample_users():
    """Add sample users with name-based usernames"""
    
    # Sample users with realistic Kenyan names
    sample_users = [
        {
            'full_name': 'John Kamau',
            'username': 'john.kamau',
            'email': 'john.kamau@naismart.com',
            'role': 'employee',
            'password': 'password123'
        },
        {
            'full_name': 'Mary Wanjiku',
            'username': 'mary.wanjiku', 
            'email': 'mary.wanjiku@naismart.com',
            'role': 'employee',
            'password': 'password123'
        },
        {
            'full_name': 'Peter Ochieng',
            'username': 'peter.ochieng',
            'email': 'peter.ochieng@naismart.com',
            'role': 'employee',
            'password': 'password123'
        },
        {
            'full_name': 'Grace Akinyi',
            'username': 'grace.akinyi',
            'email': 'grace.akinyi@naismart.com',
            'role': 'employee',
            'password': 'password123'
        },
        {
            'full_name': 'David Mwangi',
            'username': 'david.mwangi',
            'email': 'david.mwangi@naismart.com',
            'role': 'employee',
            'password': 'password123'
        },
        {
            'full_name': 'Sarah Njeri',
            'username': 'sarah.njeri',
            'email': 'sarah.njeri@naismart.com',
            'role': 'passenger',
            'password': 'password123'
        },
        {
            'full_name': 'James Kiprotich',
            'username': 'james.kiprotich',
            'email': 'james.kiprotich@naismart.com',
            'role': 'passenger',
            'password': 'password123'
        }
    ]
    
    with app.app_context():
        try:
            users_added = 0
            users_skipped = 0
            
            print("🏦 Adding Sample Users with Name-based Usernames")
            print("=" * 60)
            
            for user_data in sample_users:
                # Check if user already exists
                existing_user = User.query.filter_by(username=user_data['username']).first()
                if existing_user:
                    print(f"⚠️  User '{user_data['username']}' already exists - skipping")
                    users_skipped += 1
                    continue
                
                # Create new user
                new_user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    role=user_data['role'],
                    full_name=user_data['full_name'],
                    status='active'
                )
                new_user.set_password(user_data['password'])
                
                db.session.add(new_user)
                print(f"✅ Added: {user_data['username']} ({user_data['full_name']}) - {user_data['role']}")
                users_added += 1
            
            # Commit all changes
