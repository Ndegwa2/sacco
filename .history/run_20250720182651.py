import traceback
import os
import sys
from flask import Flask, request, redirect, render_template, flash, url_for, send_from_directory, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import csv
from server.models.employee_payment import EmployeePayment
from flask_login import current_user
from flask_migrate import Migrate

# Extend system path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config import db, configure_app
from server.models import User, Vehicle, Route, Booking, EmployeePayment
from server.models.user import SaccoMember
from server.models.fleet import Fleet
from server.models.route_assignment import AssignedRoute

# Flask app initialization
app = Flask(__name__, static_folder="Client", static_url_path="/")
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')  # Fallback for local testing

# Configure and initialize extensions
configure_app(app)
db.init_app(app)
Migrate(app, db)

# Initialize database
with app.app_context():
    db.create_all()

# Login manager setup
    from config import db
    from server.models.route_assignment import AssignedRoute

    # Create a test entry
    assignment = AssignedRoute(employee_id=2, route_id=1)
    db.session.add(assignment)
    db.session.commit()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------------ ROUTES ------------------------

@app.route("/")
def index():
    return send_from_directory("Client", "index.html")

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

        # Instead of print, insert into DB
        new_booking = Booking(
            route=route,
            pickup=pickup,
            dropoff=dropoff,
            date=travel_date,
            time=travel_time,
            name=name,
            contact=contact,
            status="confirmed"  # NEW!
        )
        db.session.add(new_booking)
        db.session.commit()

        flash("Booking confirmed! You’ll receive details shortly.", "success")
        return render_template('Client/Booking.html')

    return render_template('booking.html')

@app.route("/confirmation")
def confirmation():
    return "<h1>Thank you for booking with NaiSmart!</h1><p>Your trip has been reserved.</p>"

@app.route("/dashboard_employee.html")
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect("/")
    return render_template("employee/dashboard_employee.html")

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

@app.route("/dashboard_passenger.html")
@login_required
def passenger_dashboard():
    if current_user.role != 'passenger':
        flash("Unauthorized access", "error")
        return redirect("/")
    return send_from_directory("Client", "dashboard_passenger.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

# ---------------------- ADMIN ROUTES ----------------------

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect("/")
    users = User.query.all()
    routes = Route.query.all()
    bookings = Booking.query.filter_by(status='confirmed').all()  # updated!

    return render_template('admin/admin.html', users=users, routes=routes, bookings=bookings)

@app.route('/admin/fleet')
@login_required
def fleet_management():
    return render_template('admin/FleetManagement.html')

@app.route('/admin/fleet/add', methods=['POST'])
def add_fleet():
    plate = request.form.get("plate_number")
    model = request.form.get("vehicle_model")
    route = request.form.get("assigned_route")
    status = request.form.get("status")

    new_vehicle = Fleet(
        plate_number=plate,
        vehicle_model=model,
        assigned_route=route,
        status=status
    )
    db.session.add(new_vehicle)
    db.session.commit()

    flash("Vehicle added successfully!")
    return redirect(url_for('serve_static_client', filename='admin/FleetManagement.html'))

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

    # ✅ Return this if successful
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
    return render_template('admin/reports.html')

# ------------------ STATIC FILE HANDLER ------------------

@app.route('/client/<path:filename>')
def serve_static_client(filename):
    return send_from_directory('Client', filename)


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
# ------------------ RUN THE APP ------------------

if __name__ == "__main__":
    app.run(debug=True)


