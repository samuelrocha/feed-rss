from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
app = Flask(__name__)

app.config.from_object('config')

db.init_app(app)
login_manager.init_app(app)

migrate = Migrate(app, db)

from app.models import tables
from app.controllers import default, helpers