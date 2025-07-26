from flask import Flask
from sqlalchemy import inspect
from config import db, configure_app

app = Flask(__name__)
configure_app(app)
db.init_app(app)

with app.app_context():
    inspector = inspect(db.engine)
    
    # Get columns for assigned_route table
    columns = inspector.get_columns('assigned_route')
    print("Columns in assigned_route table:")
    for column in columns:
        print(f"  {column['name']}: {column['type']}")
    
    # Get foreign keys
    foreign_keys = inspector.get_foreign_keys('assigned_route')
    print("\nForeign keys in assigned_route table:")
    for fk in foreign_keys:
        print(f"  {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")