from extensions import db
from models import User, Knight, Spy
from models.utils import today
from services.spy_service import is_revealed

def get_knight(user_id):
    return db.session.get(Knight, user_id)


def has_active_reveal(viewer_id, target_id):
    return db.session.query(Spy.id).filter_by(
        viewer_id=viewer_id, target_id=target_id, reveal_date=today()
    ).first() is not None


def can_see_stats(viewer: User, knight: Knight):
    if viewer.role == "noble":
        return True
    if viewer.id == knight.user_id:
        return True
    if knight.knight_type == "white":
        return True
    if viewer.role == "knight":
        target = db.session.get(User, knight.user_id)
        if target.house_id == viewer.house_id and viewer.house_id is not None:
            return True
        return is_revealed(viewer.id, knight.user_id)
    return False


def update_stats(knight: Knight, stats: dict):
    knight.set_stats(stats)
    