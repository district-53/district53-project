from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from storage import Storage

db = SQLAlchemy()
login_manager = LoginManager()
storage = Storage()