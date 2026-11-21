from extensions import db
from models import User, Knight, Spy
from models.utils import today
from services.spy_service import is_revealed

STAT_NAMES = ("strength", "dexterity", "constitution")
STAT_MIN, STAT_MAX = 1, 100

def get_knight(user_id):
    return db.session.get(Knight, user_id)


def has_active_reveal(viewer_id, target_id):
    return db.session.query(Spy.id).filter_by(
        viewer_id=viewer_id, target_id=target_id, reveal_date=today()
    ).first() is not None


def can_see_stats(viewer, knight):
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


def update_stats(knight, stats):
    for name in STAT_NAMES:
        value = stats.get(name)
        if value is None or not STAT_MIN <= value <= STAT_MAX:
            raise ValueError(f"{name.capitalize()} must be a number from {STAT_MIN} to {STAT_MAX}.")

    knight.strength = stats["strength"]
    knight.dexterity = stats["dexterity"]
    knight.constitution = stats["constitution"]