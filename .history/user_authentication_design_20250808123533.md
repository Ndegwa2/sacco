# User Authentication and Role-Based Access Control System Design

## Overview
This document outlines the design for the user authentication and role-based access control system for the NaiSmart SACCO Management System. The system will support three user roles: Admin, Employee, and Passenger, each with specific permissions and access levels.

## Current Implementation Analysis

### Authentication Flow
1. Users register with username, email, password, full name, and role
2. Passwords are hashed using werkzeug.security
3. Login uses Flask-Login for session management
4. Role-based redirection after login:
   - Admin: `/admin`
   - Employee: `/dashboard_employee.html`
   - Passenger: `/dashboard_passenger.html`

### Existing Models
The `User` model already includes:
- id (Integer, Primary Key)
- username (String, Unique, Not Null)
- email (String, Unique)
- password_hash (String, Not Null)
- role (String, Default: 'passenger')
- full_name (String, Nullable)
- status (String, Default: 'active')

## Proposed Enhancements

### 1. Enhanced User Model
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='passenger')  # admin, employee, passenger
    full_name = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(50), default='active')   # active, inactive, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user')
    employee_payments = db.relationship('EmployeePayment', backref='employee')
    performances = db.relationship('Performance', backref='employee')
    assigned_routes = db.relationship('AssignedRoute', foreign_keys='AssignedRoute.employee_id', backref='employee')
    driver_logs = db.relationship('DriverLog', backref='driver')
    vehicle_health_checks = db.relationship('VehicleHealth', backref='driver')
    created_assignments = db.relationship('AssignedRoute', foreign_keys='AssignedRoute.created_by', backref='creator')
    created_vehicle_route_assignments = db.relationship('VehicleRouteAssignment', foreign_keys='VehicleRouteAssignment.assigned_by', backref='admin')
```

### 2. Authentication Endpoints

#### Login Route
```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.status == 'active':
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            flash("Login successful!", "success")
            
            # Role-based redirection
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'employee':
                return redirect(url_for('employee_dashboard'))
            elif user.role == 'passenger':
