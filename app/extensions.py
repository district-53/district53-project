from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from storage import Storage

db = SQLAlchemy()
login_manager = LoginManager()
storage = Storage()