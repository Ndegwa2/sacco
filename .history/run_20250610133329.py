import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, request, redirect, render_template, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from server.models.user import User
from config import db, app, login_manager

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect("/admin")  # Or any other page

        flash("Invalid username or password.")
        return redirect("/login")

    return render_template("login.html")  # this loads your login HTML file

    logout_user()
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))
if __name__ == "__main__":
    app.run(debug=True)