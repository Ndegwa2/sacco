from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models.user import user
app = Flask(__name__)
app.config['SECRET_KEY'] = 'GX!Caat6BP#AUs7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nais mart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))