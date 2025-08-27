from config import db
from datetime import datetime

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Link to authenticated user
    route = db.Column(db.String(100), nullable=False)
    pickup = db.Column(db.String(100), nullable=False)
    dropoff = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)  # Proper Date type
    time = db.Column(db.Time, nullable=False)  # Proper Time type
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Track when booking was created
    
    # Relationship to User model
    user = db.relationship('User', backref='bookings')
    
    @staticmethod
    def is_double_booking(route, date, time, user_id=None, name=None, contact=None):
        """
        Check if a booking is a double booking based on route, date, time, and user identification.
        
        Args:
            route (str): The route of the booking
            date (date): The date of the booking
            time (time): The time of the booking
            user_id (int, optional): The user ID for authenticated users
            name (str, optional): The name for anonymous bookings
            contact (str, optional): The contact for anonymous bookings
            
        Returns:
            bool: True if it's a double booking, False otherwise
        """
        # Base query for matching route, date, and time
        query = Booking.query.filter_by(route=route, date=date, time=time)
        
        # For authenticated users, check by user_id
        if user_id:
            query = query.filter_by(user_id=user_id)
        # For anonymous users, check by name and contact
        elif name and contact:
            query = query.filter_by(name=name, contact=contact)
        else:
            # If we don't have proper identification, we can't reliably check for double booking
            return False
            
        # If any matching booking exists, it's a double booking
        return query.first() is not None