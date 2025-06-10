import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, request, redirect, render_template, flash, url_for, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required
from server.models.user import User
from config import db, login_manager

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect("/client/index.html")  # or dashboard page
        else:
            flash("Invalid username or password.")
            return redirect("/login")

    return send_from_directory("Client", "login.html")

@app.route('/client/<path:filename>')
def serve_static_client(filename):
    return send_from_directory('Client', filename)

@app.route('/register', methods=['GET', 'POST'])
def register():
    from config import db  # Prevent circular imports
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or Email already exists.", "error")
            return redirect(url_for('register'))

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

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