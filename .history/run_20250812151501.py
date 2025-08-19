import traceback
import os
import sys
from flask import Flask, request, redirect, render_template, flash, url_for, send_from_directory, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import csv
from server.models.employee_payment import EmployeePayment
from flask_login import current_user
from flask_migrate import Migrate

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Extend system path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config import db, configure_app
from server.models import User, Vehicle, Route, Booking, EmployeePayment, Performance
from server.models.user import SaccoMember
from server.models.route_assignment import AssignedRoute
from server.models.driver_log import DriverLog
from server.models.vehicle_health import VehicleHealth
from server.models.vehicle_route_assignment import VehicleRouteAssignment

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'Ndegwa_Sacco')  # Fallback for local testing

# Configure and initialize extensions
configure_app(app)
db.init_app(app)
Migrate(app, db)


# Initialize database
with app.app_context():
    db.create_all()

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------------ ROUTES ------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash("Login successful!", "success")

                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif user.role == 'employee':
                    return redirect("/dashboard_employee.html")
                elif user.role == 'passenger':
                    return redirect("/dashboard_passenger.html")
                else:
                    return redirect("/index.html")

            flash("Invalid username or password", "error")
            return redirect("/login")

        return render_template("login.html")
    except Exception as e:
        print("❌ Login error:", e)
        traceback.print_exc()
        return "Login failed", 500

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return redirect("/register")

        user = User(username=username, email=email, role=role, full_name=full_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect("/login")

    return render_template("register.html")

@app.route("/booking", methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        # Collect booking form data
        route = request.form.get('route')
        pickup = request.form.get('pickup')
        dropoff = request.form.get('dropoff')
        travel_date = request.form.get('date')
        travel_time = request.form.get('time')
        name = request.form.get('name')
        contact = request.form.get('contact')

        # Convert string date and time to proper types
        from datetime import datetime
        try:
            booking_date = datetime.strptime(travel_date, '%Y-%m-%d').date()
            booking_time = datetime.strptime(travel_time, '%H:%M').time()
        except ValueError as e:
            flash(f"Invalid date or time format: {e}", "error")
            return redirect(url_for('booking'))

        # Create booking with user_id if user is authenticated
        new_booking = Booking(
            user_id=current_user.id if current_user.is_authenticated else None,
            route=route,
            pickup=pickup,
            dropoff=dropoff,
            date=booking_date,
            time=booking_time,
            name=name,
            contact=contact,
            status="confirmed"
        )
        db.session.add(new_booking)
        db.session.commit()
        
        # Redirect to confirmation page after successful booking
        return redirect(url_for('confirmation'))

    # For GET requests, opted to serve the static Booking.html file from Client directory
    return send_from_directory("Client", "Booking.html")

@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")

@app.route("/dashboard_employee.html")
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect("/")
    
    # Get employee's assigned routes
    assigned_routes = AssignedRoute.query.filter_by(employee_id=current_user.id).all()
    total_routes = len(assigned_routes)
    
    # Get employee's driver logs for consistent data source
    driver_logs = DriverLog.query.filter_by(driver_id=current_user.id).all()
    total_trips = sum(log.trips_completed for log in driver_logs) if driver_logs else 0
    total_earnings = sum(log.total_earnings for log in driver_logs) if driver_logs else 0
    
    # Get total distance from the same driver logs
    total_distance = sum(log.total_distance for log in driver_logs) if driver_logs else 0
    
    # Get recent vehicle health checks
    recent_health_checks = VehicleHealth.query.filter_by(driver_id=current_user.id).order_by(VehicleHealth.check_date.desc()).limit(5).all()
    health_checks_count = len(recent_health_checks)
    
    # Get payment summary
    payments = EmployeePayment.query.filter_by(employee_id=current_user.id).all()
    total_payments = len(payments)
    
    return render_template("employee/dashboard_employee.html",
                         employee_name=current_user.get_full_name(),
                         total_routes=total_routes,
                         total_trips=total_trips,
                         total_earnings=total_earnings,
                         total_distance=total_distance,
                         health_checks_count=health_checks_count,
                         total_payments=total_payments)

@app.route("/employee/payment-summary")
@login_required
def view_payment_summary():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))

    employee_id = current_user.id
    payments = EmployeePayment.query.filter_by(employee_id=employee_id).all()

    total_trips = 0
    total_fare_collected = 0
    commission_earned = 0

    for payment in payments:
        total_trips += payment.total_trips if payment.total_trips else 0
        total_fare_collected += payment.total_fare_collected if payment.total_fare_collected else 0
        commission_earned += payment.commission_earned if payment.commission_earned else 0

    payment_summary = {
        'employee_id': employee_id,
        'total_trips': total_trips,
        'total_fare_collected': total_fare_collected,
        'commission_earned': commission_earned,
        'num_payments': len(payments)
    }
    return render_template(
        'employee/payment_summary.html',
        payment_summary=payment_summary,
        payments=payments # Pass the payments object for the table
    )
@app.route('/employee/payment_summary/export')
@login_required
def export_payment_csv():
    payments = EmployeePayment.query.filter_by(employee_id=current_user.id).all()

    # Create CSV in memory
    def generate():
        data = csv.writer()
        yield ','.join(['Date', 'Trips', 'Fare Collected (KES)', 'Commission (KES)', 'Status']) + '\n'
        for p in payments:
            yield f"{p.payment_date},{p.total_trips},{p.total_fare_collected},{p.commission_earned},{p.payment_status}\n"

    return Response(
        generate(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=payment_summary.csv'
        }
    )

    return render_template('employee/payment_summary.html', payment_summary=payment_summary)

@app.route("/dashboard_passenger.html")
@login_required
def passenger_dashboard():
    if current_user.role != 'passenger':
        flash("Unauthorized access", "error")
        return redirect("/")
    
    # Get passenger's bookings - prioritize user_id, fallback to name matching for legacy bookings
    passenger_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    
    # If no bookings found by user_id, try name matching for legacy bookings
    if not passenger_bookings:
        passenger_bookings = Booking.query.filter_by(name=current_user.get_full_name()).all()
        
        # Update legacy bookings to link with current user
        if passenger_bookings:
            for booking in passenger_bookings:
                if booking.user_id is None:  # Only update if not already linked
                    booking.user_id = current_user.id
            db.session.commit()
    
    # Calculate statistics
    total_bookings = len(passenger_bookings)
    
    # Calculate total fare based on distance (20 KES per km)
    total_fare = 0
    for booking in passenger_bookings:
        # Get the route object to access distance
        route = Route.query.filter_by(route_name=booking.route).first()
        if route and route.distance:
            # Calculate fare based on distance: 20 KES per km
            total_fare += route.distance * 20
        else:
            # Fallback for routes without distance information
            # Simple fare calculation - you can adjust this based on your business logic
            if 'Nairobi' in booking.route and 'Mombasa' in booking.route:
                total_fare += 1500  # Long distance
            elif 'Nairobi' in booking.route:
                total_fare += 500   # Medium distance
            else:
                total_fare += 200   # Short distance
    
    # Calculate reward points (1 point per 100 KSh spent)
    reward_points = int(total_fare / 100)
    
    # Get recent bookings (last 5) - use user_id for better performance
    recent_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.id.desc()).limit(5).all()
    
    # If no recent bookings by user_id, fallback to name matching
    if not recent_bookings:
        recent_bookings = Booking.query.filter_by(name=current_user.get_full_name()).order_by(Booking.id.desc()).limit(5).all()
    
    return render_template("passenger_dashboard.html",
                         passenger_name=current_user.get_full_name(),
                         total_bookings=total_bookings,
                         total_fare=total_fare,
                         reward_points=reward_points,
                         recent_bookings=recent_bookings)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/employee/performance-tracker')
@login_required
def performance_tracker():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))

    # Get performance data for the current employee
    performances = Performance.query.filter_by(employee_id=current_user.id).order_by(Performance.date.desc()).all()
    
    # Calculate summary statistics
    total_trips = sum(p.trips for p in performances) if performances else 0
    total_fare = sum(p.fare_collected for p in performances) if performances else 0
    avg_fare = round(total_fare / total_trips, 2) if total_trips > 0 else 0
    
    # Find top route
    route_counts = {}
    for p in performances:
        if p.route:
            route_counts[p.route] = route_counts.get(p.route, 0) + p.trips
    
    top_route = max(route_counts.items(), key=lambda x: x[1])[0] if route_counts else "N/A"
    
    # Create summary object
    from collections import namedtuple
    Summary = namedtuple('Summary', ['total_trips', 'total_fare', 'avg_fare', 'top_route'])
    summary = Summary(
        total_trips=total_trips,
        total_fare=round(total_fare, 2),
        avg_fare=avg_fare,
        top_route=top_route
    )
    
    # Format data for table
    table_rows = [
        {
            'date': p.date.strftime('%Y-%m-%d'),
            'trips': p.trips,
            'fare': round(p.fare_collected, 2),
            'commission': round(p.commission, 2)
        }
        for p in performances
    ]
    
    # Format data for weekly chart
    from datetime import datetime, timedelta
    import calendar
    
    # Get the last 6 weeks
    today = datetime.now().date()
    weeks = []
    for i in range(5, -1, -1):
        start_date = today - timedelta(days=today.weekday() + 7 * i)
        week_name = f"{start_date.strftime('%b %d')}"
        weeks.append((week_name, start_date, start_date + timedelta(days=6)))
    
    # Calculate trips per week
    weekly_data = []
    for week_name, start_date, end_date in weeks:
        week_trips = sum(
            p.trips for p in performances
            if isinstance(p.date, str) and start_date <= datetime.strptime(p.date, '%Y-%m-%d').date() <= end_date
            or not isinstance(p.date, str) and start_date <= p.date <= end_date
        )
        weekly_data.append({'week': week_name, 'trips': week_trips})
    
    return render_template(
        'employee/performance_tracker.html',
        summary=summary,
        table_rows=table_rows,
        weekly_data=weekly_data
    )

@app.route('/employee/performance/export')
@login_required
def export_performance_csv():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    performances = Performance.query.filter_by(employee_id=current_user.id).order_by(Performance.date.desc()).all()
    
    # Create CSV in memory
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Date', 'Trips', 'Fare Collected (KES)', 'Commission (KES)', 'Route'])
    
    for p in performances:
        writer.writerow([
            p.date.strftime('%Y-%m-%d'),
            p.trips,
            p.fare_collected,
            p.commission,
            p.route or "N/A"
        ])
    
    output = si.getvalue()
    si.close()
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=my_performance.csv"}
    )

    

# ---------------------- ADMIN ROUTES ----------------------

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect("/")
    
    # Get basic data
    users = User.query.all()
    routes = Route.query.all()
    bookings = Booking.query.filter_by(status='confirmed').all()
    
    # Calculate total revenue from Performance model
    total_revenue_performance = db.session.query(db.func.sum(Performance.fare_collected)).scalar() or 0
    
    # Calculate total revenue from EmployeePayment model
    total_revenue_payments = db.session.query(db.func.sum(EmployeePayment.total_fare_collected)).scalar() or 0
    
    # Total revenue is the sum of both
    total_revenue = total_revenue_performance + total_revenue_payments
    
    # Count active routes
    active_routes_count = Route.query.filter_by(status='active').count()
    
    # Get recent activity (last 5 bookings, payments, and performance records)
    recent_bookings = Booking.query.order_by(Booking.id.desc()).limit(5).all()
    recent_payments = EmployeePayment.query.order_by(EmployeePayment.id.desc()).limit(5).all()
    recent_performances = Performance.query.order_by(Performance.id.desc()).limit(5).all()
    
    # Combine and sort recent activity
    recent_activity = []
    
    for booking in recent_bookings:
        recent_activity.append({
            'type': 'booking',
            'date': booking.date.strftime('%Y-%m-%d') if booking.date else "N/A",
            'description': f"New booking: {booking.name} on route {booking.route}"
        })
    
    for payment in recent_payments:
        employee = User.query.get(payment.employee_id)
        employee_name = employee.get_full_name() if employee else "Unknown"
        recent_activity.append({
            'type': 'payment',
            'date': payment.payment_date.strftime('%Y-%m-%d') if payment.payment_date else "N/A",
            'description': f"Payment: {employee_name} received KES {payment.commission_earned}"
        })
    
    for perf in recent_performances:
        employee = User.query.get(perf.employee_id)
        employee_name = employee.get_full_name() if employee else "Unknown"
        recent_activity.append({
            'type': 'performance',
            'date': perf.date.strftime('%Y-%m-%d') if perf.date else "N/A",
            'description': f"Performance: {employee_name} collected KES {perf.fare_collected}"
        })
    
    # Sort by date (most recent first)
    # Now all dates are strings, so sorting will work consistently
    recent_activity = sorted(recent_activity, key=lambda x: x['date'], reverse=True)[:5]
    
    # Get total bookings count
    total_bookings = Booking.query.count()

    return render_template('admin/admin.html',
                          users=users,
                          routes=routes,
                          bookings=bookings,
                          total_revenue=total_revenue,
                          active_routes_count=active_routes_count,
                          recent_activity=recent_activity,
                          total_bookings=total_bookings)

@app.route('/admin/fleet')
@login_required
def fleet_management():
    vehicles = Vehicle.query.all()
    return render_template('admin/VehicleManagement.html', vehicles=vehicles)

@app.route('/admin/fleet/add', methods=['POST'])
def add_fleet():
    plate = request.form.get("plate_number")
    model = request.form.get("vehicle_model")
    route = request.form.get("assigned_route")
    status = request.form.get("status")

    new_vehicle = Vehicle(
        plate_number=plate,
        vehicle_model=model,
        assigned_route=route,
        status=status
    )
    db.session.add(new_vehicle)
    db.session.commit()

    flash("Vehicle added successfully!")
    return redirect(url_for('fleet_management'))

@app.route('/admin/routes')
@login_required
def manage_routes():
    routes = Route.query.all()
    return render_template('admin/ManageRoute.html', routes=routes)

@app.route('/admin/routes/add', methods=['POST'])
@login_required
def add_route():
    route_name = request.form.get("route_name")
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    stops = request.form.get("stops")
    status = request.form.get("status")

    new_route = Route(
        route_name=route_name,
        origin=origin,
        destination=destination,
        stops=stops,
        status=status
    )
    db.session.add(new_route)
    db.session.commit()

    flash("Route added successfully!")

    #  Return this if successful
    return redirect(url_for('manage_routes'))

@app.route('/admin/fare-records')
@login_required
def fare_records():
    return render_template('admin/FareRecords.html')


@app.route('/admin/sacco-members', methods=['GET', 'POST'])
@login_required
def sacco_members():
    if request.method == 'POST':
        # Capture form data
        full_name = request.form['full_name']
        id_number = request.form['id_number']
        email = request.form['email']
        phone = request.form['phone']
        shareholding = request.form['shareholding'].replace(',', '')

        new_member = SaccoMember(
            full_name=full_name,
            id_number=id_number,
            email=email,
            phone=phone,
            shareholding=shareholding
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('sacco_members'))

    # For GET request
    members = SaccoMember.query.all()
    return render_template('admin/sacco_members.html', members=members)

@app.route('/admin/staff', methods=['GET', 'POST'])
@login_required
def staff_management():
    if request.method == 'POST':
        # Capture form data
        full_name = request.form['full_name']
        staff_id = request.form['staff_id']
        role = request.form['role']
        contact = request.form['contact']
        status = request.form['status']

        # Create a new User object
        new_staff = User(username=staff_id, email=contact, role=role, full_name=full_name, status=status)
        new_staff.set_password("default_password") # Set a default password
        db.session.add(new_staff)
        db.session.commit()

        flash("Staff member added successfully!", "success")
        return redirect(url_for('staff_management'))

    staff_members = User.query.all()
    return render_template('admin/staff_management.html', staff=staff_members)

@app.route('/admin/reports')
@login_required
def reports():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Calculate total revenue for the current month
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Get revenue from Performance model for current month
    monthly_performance_revenue = db.session.query(db.func.sum(Performance.fare_collected)).filter(
        db.extract('month', Performance.date) == current_month,
        db.extract('year', Performance.date) == current_year
    ).scalar() or 0
    
    # Get revenue from EmployeePayment model for current month
    monthly_payment_revenue = db.session.query(db.func.sum(EmployeePayment.total_fare_collected)).filter(
        db.extract('month', EmployeePayment.payment_date) == current_month,
        db.extract('year', EmployeePayment.payment_date) == current_year
    ).scalar() or 0
    
    # Total monthly revenue
    total_monthly_revenue = monthly_performance_revenue + monthly_payment_revenue
    
    # Find most active route (route with most trips)
    route_trips = {}
    performances = Performance.query.all()
    for perf in performances:
        if perf.route:
            route_trips[perf.route] = route_trips.get(perf.route, 0) + perf.trips
    
    most_active_route = "None" if not route_trips else max(route_trips.items(), key=lambda x: x[1])[0]
    
    # Count active vehicles
    active_vehicles_count = Vehicle.query.filter_by(status='active').count()
    
    # Find top earning driver
    employee_earnings = {}
    for perf in performances:
        employee_earnings[perf.employee_id] = employee_earnings.get(perf.employee_id, 0) + perf.commission
    
    top_driver = None
    top_earnings = 0
    if employee_earnings:
        top_driver_id = max(employee_earnings.items(), key=lambda x: x[1])[0]
        top_earnings = employee_earnings[top_driver_id]
        top_driver = User.query.get(top_driver_id)
    
    # Get recent activity log
    recent_activities = []
    
    # Add recent performance records
    recent_performances = Performance.query.order_by(Performance.date.desc()).limit(5).all()
    for perf in recent_performances:
        employee = User.query.get(perf.employee_id)
        employee_name = employee.get_full_name() if employee else "Unknown"
        recent_activities.append({
            'date': perf.date.strftime('%Y-%m-%d'),
            'activity': 'Fare Collection Logged',
            'details': f"KES {perf.fare_collected:,.2f} on Route: {perf.route}"
        })
    
    # Add recent fleet maintenance (placeholder - would need a maintenance model)
    # For now, we'll use fleet status changes as a proxy
    recent_fleet = Vehicle.query.order_by(Vehicle.id.desc()).limit(3).all()
    for vehicle in recent_fleet:
        recent_activities.append({
            'date': datetime.now().strftime('%Y-%m-%d'),  # Placeholder date
            'activity': 'Vehicle Status Update',
            'details': f"{vehicle.plate_number} - {vehicle.status.capitalize()}"
        })
    
    # Sort activities by date (most recent first)
    recent_activities = sorted(recent_activities, key=lambda x: x['date'], reverse=True)
    
    return render_template('admin/reports.html',
                          total_monthly_revenue=total_monthly_revenue,
                          most_active_route=most_active_route,
                          active_vehicles_count=active_vehicles_count,
                          top_driver=top_driver,
                          top_earnings=top_earnings,
                          recent_activities=recent_activities)

@app.route('/admin/performance-tracker')
@login_required
def admin_performance_tracker():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get employee filter
    selected_employee_id = request.args.get('employee_id', 'all')
    
    # Get all employees with role 'employee'
    employees = User.query.filter_by(role='employee').all()
    
    # Get performance data based on filter
    if selected_employee_id == 'all':
        performances = Performance.query.order_by(Performance.date.desc()).all()
    else:
        performances = Performance.query.filter_by(employee_id=selected_employee_id).order_by(Performance.date.desc()).all()
    
    # Calculate summary statistics
    total_trips = sum(p.trips for p in performances) if performances else 0
    total_fare = sum(p.fare_collected for p in performances) if performances else 0
    avg_fare = round(total_fare / total_trips, 2) if total_trips > 0 else 0
    
    # Find top route
    route_counts = {}
    for p in performances:
        if p.route:
            route_counts[p.route] = route_counts.get(p.route, 0) + p.trips
    
    top_route = max(route_counts.items(), key=lambda x: x[1])[0] if route_counts else "N/A"
    
    # Create summary object
    from collections import namedtuple
    Summary = namedtuple('Summary', ['total_trips', 'total_fare', 'avg_fare', 'top_route'])
    summary = Summary(
        total_trips=total_trips,
        total_fare=round(total_fare, 2),
        avg_fare=avg_fare,
        top_route=top_route
    )
    
    # Format data for table
    table_rows = []
    for p in performances:
        employee = User.query.get(p.employee_id)
        employee_name = employee.get_full_name() if employee else "Unknown"
        
        table_rows.append({
            'id': p.id,
            'employee_name': employee_name,
            'date': p.date.strftime('%Y-%m-%d'),
            'trips': p.trips,
            'fare': round(p.fare_collected, 2),
            'commission': round(p.commission, 2),
            'route': p.route or "N/A"
        })
    
    # Format data for weekly chart
    from datetime import datetime, timedelta
    
    # Get the last 6 weeks
    today = datetime.now().date()
    weeks = []
    for i in range(5, -1, -1):
        start_date = today - timedelta(days=today.weekday() + 7 * i)
        week_name = f"{start_date.strftime('%b %d')}"
        weeks.append((week_name, start_date, start_date + timedelta(days=6)))
    
    # Calculate trips per week
    weekly_data = []
    for week_name, start_date, end_date in weeks:
        if selected_employee_id == 'all':
            # Use database-level date filtering to avoid type comparison issues
            week_trips = sum(
                p.trips for p in Performance.query.filter(
                    Performance.date >= start_date,
                    Performance.date <= end_date
                ).all()
            )
        else:
            # Use database-level date filtering to avoid type comparison issues
            week_trips = sum(
                p.trips for p in Performance.query.filter(
                    Performance.date >= start_date,
                    Performance.date <= end_date,
                    Performance.employee_id == selected_employee_id
                ).all()
            )
        weekly_data.append({'week': week_name, 'trips': week_trips})
    
    return render_template(
        'admin/performance_tracker.html',
        summary=summary,
        table_rows=table_rows,
        weekly_data=weekly_data,
        employees=employees,
        selected_employee_id=selected_employee_id
    )

@app.route('/admin/performance/export')
@login_required
def admin_export_performance_csv():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    employee_id = request.args.get('employee_id', 'all')
    
    if employee_id == 'all':
        performances = Performance.query.order_by(Performance.date.desc()).all()
        filename = "all_employees_performance.csv"
    else:
        performances = Performance.query.filter_by(employee_id=employee_id).order_by(Performance.date.desc()).all()
        employee = User.query.get(employee_id)
        employee_name = employee.get_full_name() if employee else "Unknown"
        filename = f"{employee_name}_performance.csv"
    
    # Create CSV in memory
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Employee', 'Date', 'Trips', 'Fare Collected (KES)', 'Commission (KES)', 'Route'])
    
    for p in performances:
        employee = User.query.get(p.employee_id)
        employee_name = employee.get_full_name() if employee else "Unknown"
        
        writer.writerow([
            employee_name,
            p.date.strftime('%Y-%m-%d'),
            p.trips,
            p.fare_collected,
            p.commission,
            p.route or "N/A"
        ])
    
    output = si.getvalue()
    si.close()
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.route('/admin/performance/add', methods=['GET', 'POST'])
@login_required
def admin_add_performance():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        date_str = request.form.get('date')
        trips = request.form.get('trips')
        fare_collected = request.form.get('fare_collected')
        commission = request.form.get('commission')
        route = request.form.get('route')
        
        from datetime import datetime
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        new_performance = Performance(
            employee_id=employee_id,
            date=date,
            trips=trips,
            fare_collected=fare_collected,
            commission=commission,
            route=route
        )
        
        db.session.add(new_performance)
        db.session.commit()
        
        flash("Performance record added successfully!", "success")
        return redirect(url_for('admin_performance_tracker'))
    
    employees = User.query.filter_by(role='employee').all()
    routes = Route.query.all()
    
    return render_template(
        'admin/add_performance.html',
        employees=employees,
        routes=routes
    )

@app.route('/admin/performance/edit/<int:performance_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_performance(performance_id):
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    performance = Performance.query.get_or_404(performance_id)
    
    if request.method == 'POST':
        performance.employee_id = request.form.get('employee_id')
        date_str = request.form.get('date')
        performance.trips = request.form.get('trips')
        performance.fare_collected = request.form.get('fare_collected')
        performance.commission = request.form.get('commission')
        performance.route = request.form.get('route')
        
        from datetime import datetime
        performance.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        db.session.commit()
        
        flash("Performance record updated successfully!", "success")
        return redirect(url_for('admin_performance_tracker'))
    
    employees = User.query.filter_by(role='employee').all()
    routes = Route.query.all()
    
    return render_template(
        'admin/edit_performance.html',
        performance=performance,
        employees=employees,
        routes=routes
    )

@app.route('/admin/performance/delete/<int:performance_id>')
@login_required
def admin_delete_performance(performance_id):
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    performance = Performance.query.get_or_404(performance_id)
    db.session.delete(performance)
    db.session.commit()
    
    flash("Performance record deleted successfully!", "success")
    return redirect(url_for('admin_performance_tracker'))

@app.route('/admin/dashboard-data')
@login_required
def admin_dashboard_data():
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403
    
    # Calculate total revenue from Performance model
    total_revenue_performance = db.session.query(db.func.sum(Performance.fare_collected)).scalar() or 0
    
    # Calculate total revenue from EmployeePayment model
    total_revenue_payments = db.session.query(db.func.sum(EmployeePayment.total_fare_collected)).scalar() or 0
    
    # Total revenue is the sum of both
    total_revenue = total_revenue_performance + total_revenue_payments
    
    # Count active routes
    active_routes_count = Route.query.filter_by(status='active').count()
    
    # Get recent activity (last 5 bookings, payments, and performance records)
    recent_bookings = Booking.query.order_by(Booking.id.desc()).limit(5).all()
    recent_payments = EmployeePayment.query.order_by(EmployeePayment.id.desc()).limit(5).all()
    recent_performances = Performance.query.order_by(Performance.id.desc()).limit(5).all()
    
    # Combine and sort recent activity
    recent_activity = []
    
    for booking in recent_bookings:
        recent_activity.append({
            'type': 'booking',
            'date': booking.date.strftime('%Y-%m-%d') if booking.date else "N/A",
            'description': f"New booking: {booking.name} on route {booking.route}"
        })
    
    for payment in recent_payments:
        employee = User.query.get(payment.employee_id)
        employee_name = employee.get_full_name() if employee else "Unknown"
        recent_activity.append({
            'type': 'payment',
            'date': payment.payment_date.strftime('%Y-%m-%d') if payment.payment_date else "N/A",
            'description': f"Payment: {employee_name} received KES {payment.commission_earned}"
        })
    
    for perf in recent_performances:
        employee = User.query.get(perf.employee_id)
        employee_name = employee.get_full_name() if employee else "Unknown"
        recent_activity.append({
            'type': 'performance',
            'date': perf.date.strftime('%Y-%m-%d') if perf.date else "N/A",
            'description': f"Performance: {employee_name} collected KES {perf.fare_collected}"
        })
    
    # Sort by date (most recent first)
    # Now all dates are strings, so sorting will work consistently
    recent_activity = sorted(recent_activity, key=lambda x: x['date'], reverse=True)[:5]
    
    # Get total bookings count
    total_bookings = Booking.query.count()
    
    # Return JSON response
    from flask import jsonify
    return jsonify({
        'total_revenue': total_revenue,
        'active_routes_count': active_routes_count,
        'recent_activity': recent_activity,
        'total_bookings': total_bookings
    })

# ------------------ STATIC FILE HANDLER ------------------

@app.route('/client/<path:filename>')
def serve_static_client(filename):
    return send_from_directory('Client', filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'Naismart Logo.png', mimetype='image/vnd.microsoft.icon')


@app.route('/employee/assigned-routes')
@login_required
def view_assigned_routes():
    if current_user.role != 'employee':
        return redirect(url_for('login'))

    assignments = AssignedRoute.query.filter_by(employee_id=current_user.id).all()
    return render_template('employee/assigned_routes.html', assigned_routes=assignments)
import csv
from io import StringIO
from flask import Response

@app.route("/employee/assigned-routes/export")
@login_required
def export_assigned_routes():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))

    assignments = AssignedRoute.query.filter_by(employee_id=current_user.id).all()

    # Create in-memory CSV
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["Route Name", "Origin", "Destination", "Date Assigned"])

    for a in assignments:
        if a.route:
            writer.writerow([
                a.route.route_name,
                a.route.origin,
                a.route.destination,
                a.date_assigned.strftime('%Y-%m-%d')
            ])
        else:
            writer.writerow(["N/A", "N/A", "N/A", a.date_assigned.strftime('%Y-%m-%d')])

    output = si.getvalue()
    si.close()

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=assigned_routes.csv"}
    )

# ------------------ DRIVER LOG ROUTES ------------------

@app.route('/employee/driver-log')
@login_required
def driver_log():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get assigned routes for the current driver
    assigned_routes = AssignedRoute.query.filter_by(
        employee_id=current_user.id,
        status='active'
    ).all()
    
    # Get vehicles from Vehicle model instead of Vehicle model
    vehicles = Vehicle.query.filter_by(status='active').all()
    
    # Get recent logs for this driver
    from datetime import datetime, timedelta
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)
    
    recent_logs = DriverLog.query.filter(
        DriverLog.driver_id == current_user.id,
        DriverLog.log_date >= seven_days_ago
    ).order_by(DriverLog.log_date.desc()).all()
    
    # Calculate weekly summary
    weekly_earnings = sum(log.total_earnings for log in recent_logs)
    weekly_distance = sum(log.total_distance for log in recent_logs)
    weekly_trips = sum(log.trips_completed for log in recent_logs)
    
    return render_template(
        'employee/driver_log.html',
        assigned_routes=assigned_routes,
        vehicles=vehicles,
        recent_logs=recent_logs,
        weekly_earnings=weekly_earnings,
        weekly_distance=weekly_distance,
        weekly_trips=weekly_trips,
        current_date=today.strftime('%Y-%m-%d')
    )

@app.route('/employee/driver-log/submit', methods=['POST'])
@login_required
def submit_driver_log():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get form data
    route_id = request.form.get('route_id')
    vehicle_id = request.form.get('vehicle_id')
    starting_mileage = float(request.form.get('starting_mileage'))
    ending_mileage = float(request.form.get('ending_mileage'))
    total_distance = float(request.form.get('total_distance'))
    total_earnings = float(request.form.get('total_earnings'))
    fuel_cost = float(request.form.get('fuel_cost') or 0)
    maintenance_cost = float(request.form.get('maintenance_cost') or 0)
    net_earnings = float(request.form.get('net_earnings'))
    trips_completed = int(request.form.get('trips_completed'))
    passengers_served = int(request.form.get('passengers_served') or 0)
    notes = request.form.get('notes')
    
    # Create new driver log
    from datetime import datetime
    new_log = DriverLog(
        driver_id=current_user.id,
        vehicle_id=vehicle_id,
        route_id=route_id,
        log_date=datetime.now().date(),
        starting_mileage=starting_mileage,
        ending_mileage=ending_mileage,
        total_distance=total_distance,
        total_earnings=total_earnings,
        fuel_cost=fuel_cost,
        maintenance_cost=maintenance_cost,
        net_earnings=net_earnings,
        trips_completed=trips_completed,
        passengers_served=passengers_served,
        notes=notes
    )
    
    db.session.add(new_log)
    db.session.commit()
    
    flash("Daily log submitted successfully!", "success")
    return redirect(url_for('driver_log'))

@app.route('/employee/driver-log/export')
@login_required
def export_driver_logs():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get all logs for this driver
    logs = DriverLog.query.filter_by(driver_id=current_user.id).order_by(DriverLog.log_date.desc()).all()
    
    # Create CSV in memory
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow([
        'Date', 'Route', 'Vehicle', 'Distance (km)',
        'Total Earnings (KES)', 'Fuel Cost (KES)', 'Maintenance Cost (KES)',
        'Net Earnings (KES)', 'Trips Completed', 'Passengers Served'
    ])
    
    for log in logs:
        route = Route.query.get(log.route_id)
        vehicle = Vehicle.query.get(log.vehicle_id)
        
        writer.writerow([
            log.log_date.strftime('%Y-%m-%d'),
            route.route_name if route else "N/A",
            vehicle.plate_number if vehicle else "N/A",
            log.total_distance,
            log.total_earnings,
            log.fuel_cost,
            log.maintenance_cost,
            log.net_earnings,
            log.trips_completed,
            log.passengers_served
        ])
    
    output = si.getvalue()
    si.close()
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=driver_logs.csv"}
    )

# ------------------ VEHICLE HEALTH CHECK ROUTES ------------------

@app.route('/employee/vehicle-health')
@login_required
def vehicle_health():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get vehicles from Vehicle model instead of Vehicle model
    vehicles = Vehicle.query.filter_by(status='active').all()
    
    # Get recent health checks for this driver
    from datetime import datetime
    recent_checks = VehicleHealth.query.filter_by(driver_id=current_user.id).order_by(VehicleHealth.check_date.desc()).limit(5).all()
    
    return render_template(
        'employee/vehicle_health.html',
        vehicles=vehicles,
        recent_checks=recent_checks,
        current_date=datetime.now().strftime('%Y-%m-%d')
    )

@app.route('/employee/vehicle-health/submit', methods=['POST'])
@login_required
def submit_vehicle_health():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get form data
    vehicle_id = request.form.get('vehicle_id')
    engine_condition = int(request.form.get('engine_condition'))
    brake_condition = int(request.form.get('brake_condition'))
    tire_condition = int(request.form.get('tire_condition'))
    lights_condition = int(request.form.get('lights_condition'))
    body_condition = int(request.form.get('body_condition'))
    fuel_level = int(request.form.get('fuel_level'))
    oil_level = int(request.form.get('oil_level'))
    coolant_level = int(request.form.get('coolant_level'))
    issues_noted = request.form.get('issues_noted')
    maintenance_needed = 'maintenance_needed' in request.form
    
    # Create new vehicle health check
    from datetime import datetime
    new_check = VehicleHealth(
        vehicle_id=vehicle_id,
        driver_id=current_user.id,
        check_date=datetime.now(),
        engine_condition=engine_condition,
        brake_condition=brake_condition,
        tire_condition=tire_condition,
        lights_condition=lights_condition,
        body_condition=body_condition,
        fuel_level=fuel_level,
        oil_level=oil_level,
        coolant_level=coolant_level,
        issues_noted=issues_noted,
        maintenance_needed=maintenance_needed
    )
    
    db.session.add(new_check)
    db.session.commit()
    
    flash("Vehicle health check submitted successfully!", "success")
    return redirect(url_for('vehicle_health'))

# ------------------ ROUTE ASSIGNMENT ROUTES ------------------

@app.route('/admin/route-assignment', methods=['GET'])
@login_required
def route_assignment():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get filter parameters
    driver_id = request.args.get('driver', 'all')
    route_id = request.args.get('route', 'all')
    status = request.args.get('status', 'all')
    
    # Base query
    query = AssignedRoute.query
    
    # Apply filters
    if driver_id != 'all':
        query = query.filter(AssignedRoute.employee_id == driver_id)
    if route_id != 'all':
        query = query.filter(AssignedRoute.route_id == route_id)
    if status != 'all':
        query = query.filter(AssignedRoute.status == status)
    
    # Get assignments with filters applied
    assignments = query.order_by(AssignedRoute.date_assigned.desc()).all()
    
    # Get drivers, routes, and vehicles for the form
    drivers = User.query.filter_by(role='employee').all()
    routes = Route.query.filter_by(status='active').all()
    vehicles = Vehicle.query.all()
    
    return render_template(
        'admin/route_assignment.html',
        assignments=assignments,
        drivers=drivers,
        routes=routes,
        vehicles=vehicles
    )

@app.route('/admin/route-assignment/add', methods=['POST'])
@login_required
def add_route_assignment():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get form data
    employee_id = request.form.get('employee_id')
    route_id = request.form.get('route_id')
    vehicle_id = request.form.get('vehicle_id') or None
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    shift = request.form.get('shift')
    notes = request.form.get('notes')
    
    # Convert dates
    from datetime import datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
    
    # Create new assignment
    new_assignment = AssignedRoute(
        employee_id=employee_id,
        route_id=route_id,
        vehicle_id=vehicle_id,
        start_date=start_date,
        end_date=end_date,
        shift=shift,
        notes=notes,
        status='active',
        created_by=current_user.id
    )
    
    db.session.add(new_assignment)
    db.session.commit()
    
    flash("Route assigned successfully!", "success")
    return redirect(url_for('route_assignment'))

@app.route('/admin/route-assignment/edit/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def edit_route_assignment(assignment_id):
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get the assignment
    assignment = AssignedRoute.query.get_or_404(assignment_id)
    
    if request.method == 'POST':
        # Update assignment with form data
        assignment.employee_id = request.form.get('employee_id')
        assignment.route_id = request.form.get('route_id')
        assignment.vehicle_id = request.form.get('vehicle_id') or None
        
        # Convert dates
        from datetime import datetime
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        assignment.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        assignment.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        
        assignment.shift = request.form.get('shift')
        assignment.notes = request.form.get('notes')
        assignment.status = request.form.get('status')
        assignment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash("Assignment updated successfully!", "success")
        return redirect(url_for('route_assignment'))
    
    # Get data for form
    drivers = User.query.filter_by(role='employee').all()
    routes = Route.query.all()
    vehicles = Vehicle.query.all()
    
    return render_template(
        'admin/edit_route_assignment.html',
        assignment=assignment,
        drivers=drivers,
        routes=routes,
        vehicles=vehicles
    )

@app.route('/admin/route-assignment/delete/<int:assignment_id>')
@login_required
def delete_route_assignment(assignment_id):
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    assignment = AssignedRoute.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    
    flash("Assignment deleted successfully!", "success")
# ------------------ VEHICLE-ROUTE ASSIGNMENT ROUTES ------------------

@app.route('/admin/vehicle-route-assignment', methods=['GET'])
@login_required
def vehicle_route_assignment():
    """Admin interface for direct vehicle-to-route assignments"""
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get filter parameters
    vehicle_id = request.args.get('vehicle', 'all')
    route_id = request.args.get('route', 'all')
    status = request.args.get('status', 'all')
    
    # Base query
    query = VehicleRouteAssignment.query
    
    # Apply filters
    if vehicle_id != 'all':
        query = query.filter(VehicleRouteAssignment.vehicle_id == vehicle_id)
    if route_id != 'all':
        query = query.filter(VehicleRouteAssignment.route_id == route_id)
    if status != 'all':
        query = query.filter(VehicleRouteAssignment.status == status)
    
    # Get assignments with filters applied
    assignments = query.order_by(VehicleRouteAssignment.assigned_date.desc()).all()
    
    # Get vehicles and routes for the form
    vehicles = Vehicle.query.filter_by(status='active').all()
    routes = Route.query.filter_by(status='active').all()
    
    return render_template(
        'admin/vehicle_route_assignment.html',
        assignments=assignments,
        vehicles=vehicles,
        routes=routes
    )

@app.route('/admin/vehicle-route-assignment/add', methods=['POST'])
@login_required
def add_vehicle_route_assignment():
    """Add a new vehicle-route assignment"""
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get form data
    vehicle_id = request.form.get('vehicle_id')
    route_id = request.form.get('route_id')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    priority = request.form.get('priority', 'normal')
    notes = request.form.get('notes')
    
    # Convert dates
    from datetime import datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
    
    # Create new assignment
    new_assignment = VehicleRouteAssignment(
        vehicle_id=vehicle_id,
        route_id=route_id,
        start_date=start_date,
        end_date=end_date,
        priority=priority,
        notes=notes,
        status='active',
        assigned_by=current_user.id
    )
    
    db.session.add(new_assignment)
    db.session.commit()
    
    flash("Vehicle assigned to route successfully!", "success")
    return redirect(url_for('vehicle_route_assignment'))

@app.route('/admin/vehicle-route-assignment/edit/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def edit_vehicle_route_assignment(assignment_id):
    """Edit a vehicle-route assignment"""
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    # Get the assignment
    assignment = VehicleRouteAssignment.query.get_or_404(assignment_id)
    
    if request.method == 'POST':
        # Update assignment with form data
        assignment.vehicle_id = request.form.get('vehicle_id')
        assignment.route_id = request.form.get('route_id')
        
        # Convert dates
        from datetime import datetime
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        assignment.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        assignment.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        
        assignment.priority = request.form.get('priority', 'normal')
        assignment.notes = request.form.get('notes')
        assignment.status = request.form.get('status')
        assignment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash("Vehicle-route assignment updated successfully!", "success")
        return redirect(url_for('vehicle_route_assignment'))
    
    # Get data for form
    vehicles = Vehicle.query.all()
    routes = Route.query.all()
    
    return render_template(
        'admin/edit_vehicle_route_assignment.html',
        assignment=assignment,
        vehicles=vehicles,
        routes=routes
    )

@app.route('/admin/vehicle-route-assignment/delete/<int:assignment_id>')
@login_required
def delete_vehicle_route_assignment(assignment_id):
    """Delete a vehicle-route assignment"""
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect(url_for('login'))
    
    assignment = VehicleRouteAssignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    
    flash("Vehicle-route assignment deleted successfully!", "success")
    return redirect(url_for('vehicle_route_assignment'))
    return redirect(url_for('route_assignment'))

# ------------------ RUN THE APP ------------------

if __name__ == "__main__":
    app.run(debug=True)


