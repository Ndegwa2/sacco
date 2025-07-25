import os, sys, csv, traceback
from io import StringIO
from datetime import datetime
from flask import Flask, request, redirect, render_template, flash, url_for, send_from_directory, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate

# Extend system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Local imports
from config import db, configure_app
from server.models import User, Vehicle, Route, Booking, EmployeePayment
from server.models.user import SaccoMember
from server.models.fleet import Fleet
from server.models.route_assignment import AssignedRoute

# App setup
app = Flask(__name__, static_folder="Client", static_url_path="/")
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')

configure_app(app)
db.init_app(app)
Migrate(app, db)

with app.app_context():
    db.create_all()

# Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- HOME + AUTH ----------------

@app.route("/")
def index():
    return send_from_directory("Client", "index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            user = User.query.filter_by(username=request.form.get("username")).first()
            if user and user.check_password(request.form.get("password")):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for(
                    'admin_dashboard' if user.role == 'admin'
                    else 'employee_dashboard' if user.role == 'employee'
                    else 'index'))
            flash("Invalid credentials", "error")
            return redirect("/login")
        return render_template("login.html")
    except Exception as e:
        print("❌ Login error:", e)
        traceback.print_exc()
        return "Login failed", 500

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(username=request.form["username"]).first():
            flash("Username taken", "error")
            return redirect("/register")
        user = User(
            username=request.form["username"],
            email=request.form["email"],
            role=request.form["role"],
            full_name=request.form["full_name"]
        )
        user.set_password(request.form["password"])
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully!", "success")
        return redirect("/login")
    return render_template("register.html")


# ---------------- DASHBOARDS ----------------

@app.route("/dashboard_employee.html")
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        flash("Unauthorized", "error")
        return redirect("/")
    return render_template("employee/dashboard_employee.html")

@app.route("/dashboard_passenger.html")
@login_required
def passenger_dashboard():
    if current_user.role != 'passenger':
        flash("Unauthorized", "error")
        return redirect("/")
    return send_from_directory("Client", "dashboard_passenger.html")


# ---------------- PERFORMANCE TRACKER ----------------

@app.route("/employee/performance-tracker")
@login_required
def performance_tracker():
    if current_user.role != 'employee':
        return redirect(url_for('login'))

    table_rows = [
        {"date": "2025-07-01", "trips": 12, "fare": 4800, "commission": 960},
        {"date": "2025-07-02", "trips": 9, "fare": 3600, "commission": 720},
        {"date": "2025-07-03", "trips": 14, "fare": 5600, "commission": 1120},
    ]
    weekly_data = [
        {"week": "Week 1", "trips": 30},
        {"week": "Week 2", "trips": 45},
        {"week": "Week 3", "trips": 38},
    ]

    total_trips = sum(r["trips"] for r in table_rows)
    total_fare = sum(r["fare"] for r in table_rows)
    avg_fare = total_fare // total_trips if total_trips else 0

    summary = {
        "total_trips": total_trips,
        "total_fare": total_fare,
        "avg_fare": avg_fare,
        "top_route": "Nairobi - Rongai"
    }

    return render_template("employee/performance_tracker.html", summary=summary, table_rows=table_rows, weekly_data=weekly_data)

@app.route('/employee/performance-tracker/export')
@login_required
def export_performance_csv():
    export_rows = [
        {"date": "2025-07-01", "trips": 12, "fare": 4800, "commission": 960},
        {"date": "2025-07-02", "trips": 9, "fare": 3600, "commission": 720},
        {"date": "2025-07-03", "trips": 14, "fare": 5600, "commission": 1120},
    ]

    def generate():
        yield "Date,Trips,Fare Collected (KES),Commission (KES)\n"
        for row in export_rows:
            yield f"{row['date']},{row['trips']},{row['fare']},{row['commission']}\n"

    return Response(generate(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=performance_tracker.csv"})


# ---------------- LOGOUT ----------------

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect("/login")


# ---------------- STATIC ROUTE ----------------

@app.route("/client/<path:filename>")
def serve_static_client(filename):
    return send_from_directory("Client", filename)


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)
