#!/usr/bin/env python3
"""
Script to view and update user credentials in the Sacco Management System
This script allows you to:
1. View current users and their details
2. Update usernames from generic ones (like driver001) to actual names
3. Handle both local SQLite and production PostgreSQL databases
"""

import os
import sys
from datetime import datetime
import re

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
            
            return users
        except Exception as e:
            print(f"❌ Error viewing users: {e}")
            return []

def suggest_username_updates(users):
    """Suggest username updates based on full names"""
    suggestions = []
    
    for user in users:
        # Skip admin users
        if user.role == 'admin':
            continue
            
        # Check if username looks generic (like driver001, user123, etc.)
        if re.match(r'^(driver|user|employee)\d+$', user.username.lower()):
            full_name = user.get_full_name()
            if full_name and full_name != user.username:
                # Create username from full name
                # Convert "John Kamau" to "john.kamau" or "johnkamau"
                suggested_username = full_name.lower().replace(' ', '.').replace('-', '.')
                # Remove special characters
                suggested_username = re.sub(r'[^a-z0-9.]', '', suggested_username)
                
                suggestions.append({
                    'user_id': user.id,
                    'current_username': user.username,
                    'suggested_username': suggested_username,
                    'full_name': full_name,
                    'email': user.email,
                    'role': user.role
                })
    
    return suggestions

def display_suggestions(suggestions):
    """Display suggested username changes"""
    if not suggestions:
        print("\n✅ No generic usernames found that need updating!")
        return
    
    print(f"\n💡 Suggested Username Updates ({len(suggestions)} users):")
    print("=" * 90)
    print(f"{'ID':<4} {'Current Username':<15} {'Suggested Username':<20} {'Full Name':<20} {'Role':<10}")
    print("-" * 90)
    
    for suggestion in suggestions:
        print(f"{suggestion['user_id']:<4} {suggestion['current_username']:<15} {suggestion['suggested_username']:<20} {suggestion['full_name']:<20} {suggestion['role']:<10}")

def update_usernames(suggestions, selected_updates=None):
    """Update usernames based on suggestions"""
    if not suggestions:
        print("No suggestions to apply.")
        return
    
    with app.app_context():
        try:
            updated_count = 0
            
            for suggestion in suggestions:
                # If specific updates are selected, only process those
                if selected_updates and suggestion['user_id'] not in selected_updates:
                    continue
                
                user = User.query.get(suggestion['user_id'])
                if not user:
                    print(f"⚠️  User with ID {suggestion['user_id']} not found")
                    continue
                
                # Check if suggested username already exists
                existing_user = User.query.filter_by(username=suggestion['suggested_username']).first()
                if existing_user and existing_user.id != user.id:
                    print(f"⚠️  Username '{suggestion['suggested_username']}' already exists, skipping user {user.username}")
                    continue
                
                # Update the username
                old_username = user.username
                user.username = suggestion['suggested_username']
                
                print(f"✅ Updated: {old_username} → {suggestion['suggested_username']} ({suggestion['full_name']})")
                updated_count += 1
            
            # Commit all changes
            db.session.commit()
            print(f"\n🎉 Successfully updated {updated_count} usernames!")
            
        except Exception as e:
            print(f"❌ Error updating usernames: {e}")
            db.session.rollback()

def interactive_update():
    """Interactive mode for updating usernames"""
    print("\n🔄 Starting Interactive Username Update Process...")
    
    # View current users
    users = view_current_users()
    if not users:
        return
    
    # Get suggestions
    suggestions = suggest_username_updates(users)
    display_suggestions(suggestions)
    
    if not suggestions:
        return
    
    print("\nOptions:")
    print("1. Update all suggested usernames")
    print("2. Select specific users to update")
    print("3. Cancel")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        confirm = input(f"\nAre you sure you want to update all {len(suggestions)} usernames? (yes/no): ").strip().lower()
        if confirm == 'yes':
            update_usernames(suggestions)
        else:
            print("Update cancelled.")
    
    elif choice == '2':
        print("\nEnter the IDs of users you want to update (comma-separated):")
        ids_input = input("User IDs: ").strip()
        try:
            selected_ids = [int(id.strip()) for id in ids_input.split(',') if id.strip()]
            if selected_ids:
                update_usernames(suggestions, selected_ids)
            else:
                print("No valid IDs provided.")
        except ValueError:
            print("Invalid input. Please enter numeric IDs separated by commas.")
    
    else:
        print("Update cancelled.")

def add_new_users():
    """Add new users with proper names as usernames"""
    print("\n➕ Add New Users")
    print("Enter user details (press Enter with empty name to finish):")
    
    with app.app_context():
        try:
            users_added = 0
            
            while True:
                print("\n" + "-" * 40)
                full_name = input("Full Name: ").strip()
                if not full_name:
                    break
                
                # Generate username from full name
                username = full_name.lower().replace(' ', '.').replace('-', '.')
                username = re.sub(r'[^a-z0-9.]', '', username)
                
                # Check if username exists
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    print(f"⚠️  Username '{username}' already exists!")
                    custom_username = input(f"Enter a different username (or press Enter to skip): ").strip()
                    if custom_username:
                        username = custom_username
                    else:
                        continue
                
                email = input("Email (optional): ").strip() or None
                role = input("Role (admin/employee/passenger) [passenger]: ").strip() or 'passenger'
                password = input("Password [password123]: ").strip() or 'password123'
                
                # Create new user
                new_user = User(
                    username=username,
                    email=email,
                    role=role,
                    full_name=full_name,
                    status='active'
                )
                new_user.set_password(password)
                
                db.session.add(new_user)
                print(f"✅ Added user: {username} ({full_name}) - Role: {role}")
                users_added += 1
            
            if users_added > 0:
                db.session.commit()
                print(f"\n🎉 Successfully added {users_added} new users!")
            else:
                print("No users added.")
                
        except Exception as e:
            print(f"❌ Error adding users: {e}")
            db.session.rollback()

def reset_user_passwords():
    """Reset passwords for users who can't login"""
    print("\n🔑 Reset User Passwords")
    
    with app.app_context():
        try:
            users = User.query.all()
            print(f"\nAvailable users:")
            for user in users:
                print(f"  {user.id}: {user.username} ({user.get_full_name()}) - {user.role}")
            
            user_input = input("\nEnter user ID or username to reset password (or 'all' for all users): ").strip()
            
            if user_input.lower() == 'all':
                confirm = input("Are you sure you want to reset ALL user passwords? (yes/no): ").strip().lower()
                if confirm != 'yes':
                    print("Password reset cancelled.")
                    return
                
                new_password = input("Enter new password for all users [password123]: ").strip() or 'password123'
                
                for user in users:
                    user.set_password(new_password)
                    print(f"✅ Reset password for: {user.username}")
                
                db.session.commit()
                print(f"\n🎉 Reset passwords for all {len(users)} users!")
                print(f"🔑 New password: {new_password}")
                
            else:
                # Try to find user by ID or username
                user = None
                if user_input.isdigit():
                    user = User.query.get(int(user_input))
                else:
                    user = User.query.filter_by(username=user_input).first()
                
                if not user:
                    print(f"❌ User '{user_input}' not found.")
                    return
                
                new_password = input(f"Enter new password for {user.username} [password123]: ").strip() or 'password123'
                user.set_password(new_password)
                db.session.commit()
                
                print(f"✅ Password reset for: {user.username}")
                print(f"🔑 New password: {new_password}")
                
        except Exception as e:
            print(f"❌ Error resetting passwords: {e}")
            db.session.rollback()

def main():
    """Main function with menu options"""
    print("🏦 Sacco Management System - User Credential Manager")
    print("=" * 60)
    
    while True:
        print("\nOptions:")
        print("1. View current users")
        print("2. Update usernames (interactive)")
        print("3. Add new users")
        print("4. Reset user passwords")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            view_current_users()
        
        elif choice == '2':
            interactive_update()
        
        elif choice == '3':
            add_new_users()
        
        elif choice == '4':
            reset_user_passwords()
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()