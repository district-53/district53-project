import os
from flask import Flask
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db, login_manager
from storage import init_storage
from routes.auth_routes import auth_bp
from routes.book_routes import book_bp
from routes.picture_routes import picture_bp
from routes.exile_routes import exile_bp
from data.add_data import add_people, add_houses

def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    init_storage(app)

    import models
    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(picture_bp)
    app.register_blueprint(exile_bp)


    @app.cli.command("init-db")
    def init_db():
        import models
        db.create_all()
        print("Tables created")

    app.cli.command("add-people")(add_people)

    app.cli.command("add-houses")(add_houses)

    return app



app = create_app()

if __name__ == "__main__":
    app.run(debug=True)