import os
from flask import Flask
from flask_migrate import Migrate, upgrade

# Import the app and db from your application
from run import app, db

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Apply migrations
with app.app_context():
    # Run the migrations
    upgrade()

print("Migrations applied successfully!")