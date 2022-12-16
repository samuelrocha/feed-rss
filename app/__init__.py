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


from app.controllers import feed, helpers, errors, user, save
from app.models import Feed, List_Feed, List, News, Save, User