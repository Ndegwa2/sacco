from config import db
from datetime import datetime

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), nullable=False, unique=True)
    vehicle_model = db.Column(db.String(100), nullable=False)
    assigned_route = db.Column(db.String(100), nullable=True)  # Made nullable for flexibility
    status = db.Column(db.String(50), nullable=False, default='active')
    
    # Vehicle capacity - assuming a default capacity of 14 seats (common for matatus in Kenya)
    capacity = db.Column(db.Integer, nullable=False, default=14)
    
    # Additional fields for better vehicle management
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"Vehicle(id={self.id}, plate_number='{self.plate_number}', model='{self.vehicle_model}', status='{self.status}', capacity={self.capacity})"
    
    def is_fully_booked(self, route, date, time):
        """
        Check if this vehicle is fully booked for a specific route, date, and time.
        
        Args:
            route (str): The route name
            date (date): The booking date
            time (time): The booking time
            
        Returns:
            bool: True if the vehicle is fully booked, False otherwise
        """
        from server.models.booking import Booking
        
        # Count existing bookings for this vehicle on the same route/date/time
        booking_count = Booking.query.filter_by(
            route=route,
            date=date,
            time=time
        ).count()
        
        # Check if we've reached capacity
        return booking_count >= self.capacity