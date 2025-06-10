from run import app
from config import db
from server.models.fleet import Fleet

with app.app_context():
    db.create_all()