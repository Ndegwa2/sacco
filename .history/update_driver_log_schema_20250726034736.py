from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import os

# Extend system path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config import db, configure_app

# Flask app initialization
app = Flask(__name__)
configure_app(app)
db.init_app(app)
migrate = Migrate(app, db)

# Import models
from server.models.driver_log import DriverLog

if __name__ == '__main__':
    with app.app_context():
        # Drop the existing foreign key constraint
        db.engine.execute('ALTER TABLE driver_log DROP FOREIGN KEY driver_log_ibfk_2')
        
        # Add the new foreign key constraint
        db.engine.execute('ALTER TABLE driver_log ADD CONSTRAINT driver_log_ibfk_2 FOREIGN KEY (vehicle_id) REFERENCES fleet(id)')
        
        print("Database schema updated successfully!")