from extensions import db
from models import User, Knight, Spy
from models.utils import today
from services.spy_service import is_revealed

def get_knight(user_id):
    return db.session.get(Knight, user_id)


def update_stats(knight: Knight, stats: dict):
    knight.set_stats(stats)
    