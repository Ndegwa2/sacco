#!/usr/bin/env python3
"""
Script to link legacy bookings to users based on name matching
"""

from flask import Flask
from config import configure_app, db
from server.models.booking import Booking
from server.models.user import User

def link_legacy_bookings():
    """Link existing bookings to users where names match"""
    app = Flask(__name__)
    configure_app(app)
    db.init_app(app)
    
    with app.app_context():
        print("🔗 Linking legacy bookings to users...")
        
        # Get all bookings without user_id
        legacy_bookings = Booking.query.filter_by(user_id=None).all()
        print(f"📊 Found {len(legacy_bookings)} legacy bookings")
        
        linked_count = 0
        
        for booking in legacy_bookings:
            # Try to find a user with matching name
            user = User.query.filter_by(full_name=booking.name).first()
            if not user:
                # Try matching with username as fallback
                user = User.query.filter_by(username=booking.name).first()
            
            if user:
                booking.user_id = user.id
                linked_count += 1
                print(f"✅ Linked booking '{booking.name}' to user '{user.get_full_name()}' (ID: {user.id})")
            else:
                print(f"⚠️  No matching user found for booking '{booking.name}'")
        
        if linked_count > 0:
            db.session.commit()
            print(f"🎉 Successfully linked {linked_count} bookings to users!")
        else:
            print("ℹ️  No bookings could be linked")
        
        # Show final status
        print("\n📊 Final booking status:")
        all_bookings = Booking.query.all()
        for booking in all_bookings:
            if booking.user:
                print(f"  ✅ Booking {booking.id}: {booking.name} -> Linked to {booking.user.get_full_name()}")
            else:
                print(f"  ❌ Booking {booking.id}: {booking.name} -> No user link")

if __name__ == "__main__":
    link_legacy_bookings()