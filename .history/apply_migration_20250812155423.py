import sys
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Float
from sqlalchemy.orm import sessionmaker

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Route model
from server.models.route import Route
from config import db

# Create an engine and session
engine = create_engine('sqlite:///instance/sacco_system.db')
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the existing database schema
metadata = MetaData()
metadata.reflect(bind=engine)

# Get the route table
route_table = metadata.tables['route']

# Check if the distance column already exists
if 'distance' not in route_table.c:
    # Add the distance column
    with engine.connect() as conn:
        # SQLite specific ALTER TABLE command
        conn.execute(route_table.update().values(distance=None))
        conn.execute("ALTER TABLE route ADD COLUMN distance FLOAT")
        conn.commit()
        
    print("Distance column added successfully!")
else:
    print("Distance column already exists!")

# Close the session
session.close()