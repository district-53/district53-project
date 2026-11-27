from cli import command_reg
from config import Config
from errors import register_error_handlers
from extensions import db, login_manager, storage
from flask import Flask
from models.knights import STAT_NAMES
from routes.auth_routes import auth_bp
from routes.book_routes import book_bp
from routes.exile_routes import exile_bp
from routes.notification_routes import notifications_bp
from routes.picture_routes import picture_bp
from routes.profile_routes import profile_bp
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    storage.init_storage(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(picture_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(exile_bp)
    app.register_blueprint(notifications_bp)
    
    register_error_handlers(app)
    command_reg(app)
    
    app.jinja_env.globals["STAT_NAMES"] = STAT_NAMES
    
    return app