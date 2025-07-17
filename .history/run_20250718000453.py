import traceback
import os
import sys
from flask import Flask, request, redirect, render_template, flash, url_for, send_from_directory, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate

# Terminate any Flask process using port 5000
# os.system('fuser -k 5000/tcp > /dev/null 2>&1')

# Add server directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config import db, configure_app
from server.models import User, Vehicle, Route, Booking
from server.models.fleet import Fleet

app = Flask(__name__, static_folder="Client", static_url_path="/")
app.secret_key = os.environ.get('SECRET_KEY', None)


# Configure and initialize extensions
configure_app(app)
db.init_app(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return send_from_directory("Client", "index.html")

@app.route('/client/<path:filename>')
def serve_static_client(filename):
    return send_from_directory('Client', filename)

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
        print("\u274c Login error:", e)
        traceback.print_exc()
        return "Login failed", 500

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if User.query.filter_by(username=username).first():
            flash("Username already taken. Please choose another.", "error")
            return redirect("/register")

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can now log in.", "success")
        return redirect("/login")

    return render_template("register.html")

@app.route("/dashboard_employee.html")
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect("/")
    return send_from_directory("Client", "dashboard_employee.html")

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

@app.route('/admin/fleet')
@login_required
def fleet_management():
    return render_template('admin/FleetManagement.html')

@app.route('/admin/fare-records')
@login_required
def fare_records():
    return render_template('admin/FareRecords.html')

@app.route('/admin/sacco-members')
@login_required
def sacco_members():
    return render_template('admin/sacco_members.html')

@app.route('/admin/staff')
@login_required
def staff_management():
    return render_template('admin/staff_management.html')

@app.route('/admin/reports')
@login_required
def reports():
    return render_template('admin/reports.html')

@app.route('/admin/routes/add', methods=['POST'])
@login_required
def add_route():
    try:
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
        return redirect(url_for('manage_routes'))
    except Exception as e:
        print("\ud83d\udea8 ERROR ADDING ROUTE:", e)
        return "Something went wrong: " + str(e), 500

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Unauthorized access", "error")
        return redirect("/")
    users = User.query.all()
    routes = Route.query.all()
    bookings = Booking.query.all()
    return render_template('admin/admin.html', users=users, routes=routes, bookings=bookings)

if __name__ == "__main__":
    app.run(debug=True)
