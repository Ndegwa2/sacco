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
    
    # Add vehicle reference
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    
    # Relationship to User model
    user = db.relationship('User', backref='bookings')
    # Relationship to Vehicle model
    vehicle = db.relationship('Vehicle', backref='bookings')
    
    @staticmethod
    def is_double_booking(route, date, time, user_id=None, name=None, contact=None, vehicle_id=None):
        """
        Check if a booking is a double booking based on route, date, time, and user identification.
        
        Args:
            route (str): The route of the booking
            date (date): The date of the booking
            time (time): The time of the booking
            user_id (int, optional): The user ID for authenticated users
            name (str, optional): The name for anonymous bookings
            contact (str, optional): The contact for anonymous bookings
            vehicle_id (int, optional): The vehicle ID
            
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
    
    @staticmethod
    def is_vehicle_fully_booked(route, date, time, vehicle_id):
        """
        Check if a specific vehicle is fully booked for a given route, date, and time.
        
        Args:
            route (str): The route of the booking
            date (date): The date of the booking
            time (time): The time of the booking
            vehicle_id (int): The vehicle ID
            
        Returns:
            bool: True if the vehicle is fully booked, False otherwise
        """
        from server.models.vehicle import Vehicle
        
        # Get the vehicle to check its capacity
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            # If vehicle doesn't exist, we can't book it
            return True
            
        # Count existing bookings for this vehicle on the same route/date/time
        booking_count = Booking.query.filter_by(
            route=route,
            date=date,
            time=time,
            vehicle_id=vehicle_id
        ).count()
        
        # Check if we've reached capacity
        return booking_count >= vehicle.capacity
    
    @staticmethod
    def get_available_vehicle_for_route(route_name, date, time):
        """
        Find an available vehicle for a specific route, date, and time.
        
        Args:
            route_name (str): The name of the route
            date (date): The date of the booking
            time (time): The time of the booking
            
        Returns:
            Vehicle: An available vehicle, or None if no vehicles are available
        """
        from server.models.vehicle_route_assignment import VehicleRouteAssignment
        from server.models.route import Route
        from server.models.vehicle import Vehicle
        
        # First, find the route by name
        route = Route.query.filter_by(route_name=route_name).first()
        if not route:
            return None
            
        # Find active vehicle assignments for this route
        vehicle_assignments = VehicleRouteAssignment.query.filter_by(
            route_id=route.id,
            status='active'
        ).all()
        
        # Check each assigned vehicle to see if it has capacity
        for assignment in vehicle_assignments:
            vehicle = Vehicle.query.get(assignment.vehicle_id)
            if vehicle and vehicle.status == 'active':
                # Check if this vehicle is fully booked
                if not Booking.is_vehicle_fully_booked(route_name, date, time, vehicle.id):
                    return vehicle
                    
        # No available vehicles found
        return None