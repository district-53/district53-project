from data.add_data import seed
from extensions import db, storage


def command_reg(app):
    @app.cli.command("init-db")
    def init_db():
        """Create tables and seaweed storage"""

        db.create_all()
        if storage.is_enabled():
            storage.check_bucket()

    app.cli.command("seed")(seed)