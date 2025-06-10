import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, request, redirect, render_template, flash, url_for, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from server.models.user import User
from config import db

app = Flask(__name__, static_folder="Client", static_url_path="/")
app.secret_key = 'your_secret_key'

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect("/admin/admin.html")  # or dashboard

        return "Invalid credentials", 401

@app.route("/")
def index():
    return send_from_directory("Client", "index.html")

    return send_from_directory("Client", "login.html")

@app.route('/client/<path:filename>')
def serve_static_client(filename):
    return send_from_directory('Client', filename)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            return "User already exists", 409

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return send_from_directory("Client", "register.html")

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

if __name__ == "__main__":

    app.run(debug=True)