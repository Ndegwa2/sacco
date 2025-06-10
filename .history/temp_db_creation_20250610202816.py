from run import app
from config import db
from server.models.user import User

with app.app_context():
    db.create_all()