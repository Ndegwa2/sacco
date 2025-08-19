import sys
import os
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('instance/sacco_system.db')
cursor = conn.cursor()

# Check if the distance column already exists
cursor.execute("PRAGMA table_info(route)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]

if 'distance' not in column_names:
    # Add the distance column
    cursor.execute("ALTER TABLE route ADD COLUMN distance FLOAT")
    conn.commit()
    print("Distance column added successfully!")
else:
    print("Distance column already exists!")

# Close the connection
conn.close()