import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import render_template, redirect, url_for, request, flash
from config import db, configure_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from server.models.user import User
from flask import Flask
app = Flask(__name__)
configure_app(app)

with app.app_context():
    db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'index'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'passenger')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. You can now log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

from flask import Flask, render_template, request, redirect, url_for, flash
from config import configure_app, db
from server.models.user import User
from flask_login import LoginManager
import os

login_manager = LoginManager()
login_manager.init_app(app)

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
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))