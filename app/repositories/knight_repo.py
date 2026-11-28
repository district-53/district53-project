from extensions import db
from models import Knight


def get_knight(user_id):
    return db.session.get(Knight, user_id)
    