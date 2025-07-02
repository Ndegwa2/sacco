import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, request, redirect, render_template, flash, url_for, send_from_directory, render_template
from server.models.fleet import Fleet
from flask_login import current_user
from flask_login import LoginManager, login_user, logout_user, login_required
from server.models.user import User
from config import db

app = Flask(__name__, static_folder="Client", static_url_path="/")
app.secret_key = 'your_secret_key'
from config import configure_app
configure_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
login_manager.login_view = "login"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")

            # Redirect based on user role
            if user.role == 'admin':
                return redirect("/admin/admin.html")
            elif user.role == 'employee':
                return redirect("/dashboard_employee.html")
            else:  # default to passenger
                return redirect("/index.html")

        flash("Invalid username or password", "error")
        return redirect("/login")

    return send_from_directory("Client", "login.html")

@app.route("/")
def index():
    return send_from_directory("Client", "index.html")

@app.route('/client/<path:filename>')
def serve_static_client(filename):
    if 'templates' in filename:
        return "File not found", 404
    return send_from_directory('Client', filename)

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


    return send_from_directory("Client", "register.html")

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

@app.route('/booking', methods=['POST'])
def booking():
    if request.method == 'POST':
        print(f"Request method: {request.method}")
        print(f"Form data: {request.form}")
        route = request.form.get('route')
        pickup = request.form.get('pickup')
        dropoff = request.form.get('dropoff')
        date = request.form.get('date')
        time = request.form.get('time')
        name = request.form.get('name')
        contact = request.form.get('contact')

        # Process the booking data (e.g., store in a database)
        # For now, just print the data
        print(f"Booking Details:\nRoute: {route}\nPickup: {pickup}\nDropoff: {dropoff}\nDate: {date}\nTime: {time}\nName: {name}\nContact: {contact}")

        flash("Booking confirmed! You will receive a confirmation email shortly.", "success")
        return redirect(url_for('index'))  # Redirect to the home page after booking
    else:
        return redirect(url_for('Booking'))  # Redirect to the booking page if accessed without submitting the form

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
    fleets = Fleet.query.all()
    return render_template('Client/templates/admin/FleetManagement.html', fleets=fleets)

if __name__ == "__main__":
    app.run(debug=True)