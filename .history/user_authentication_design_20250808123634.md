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
                return redirect(url_for('passenger_dashboard'))
            else:
                return redirect(url_for('index'))
        
        flash("Invalid username or password", "error")
        return redirect(url_for('login'))
    
    return render_template("login.html")
```

#### Registration Route
```python
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        
        # Validation
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return redirect(url_for('register'))
        
        # Create user
        user = User(username=username, email=email, role=role, full_name=full_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template("register.html")
```

### 3. Role-Based Access Control Decorators

```python
from functools import wraps
from flask import abort

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Unauthorized access", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def employee_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'employee':
            flash("Unauthorized access", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def passenger_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'passenger':
            flash("Unauthorized access", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
```

### 4. Session Management

#### Logout Route
```python
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', "info")
    return redirect(url_for('login'))
```

### 5. Password Security Enhancements

```python
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(UserMixin, db.Model):
    # ... existing fields ...
    
    def set_password(self, password):
        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit")
        
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=12)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

## Role Permissions Matrix

| Feature | Admin | Employee | Passenger |
|---------|-------|----------|-----------|
| User Management | ✓ | ✗ | ✗ |
| Fleet Management | ✓ | ✗ | ✗ |
| Route Management | ✓ | ✗ | ✗ |
| Vehicle Assignment | ✓ | ✗ | ✗ |
| Booking Creation | ✓ | ✓ | ✓ |
| Booking Status View | ✓ | ✓ | ✓ |
| Performance Tracking | ✓ | ✓ | ✗ |
| Payment View | ✓ | ✓ | ✗ |
| Vehicle Health Updates | ✓ | ✓ | ✗ |
| Reports Generation | ✓ | ✗ | ✗ |

## Security Considerations

1. **Password Policy**: Minimum 8 characters with mixed case letters and numbers
2. **Session Management**: Secure session handling with Flask-Login
3. **Role Validation**: Server-side validation of user roles for all protected routes
