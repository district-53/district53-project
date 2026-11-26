from sqlalchemy import select
from extensions import db
from models import Knight, Spy
from models.utils import today


def has_used_today(knight_id: int) -> bool:
    reveal = db.session.scalar(select(Spy.id).where(Spy.viewer_id == knight_id, Spy.reveal_date == today()))
    return reveal is not None


def is_revealed(viewer_id: int, target_id: int) -> bool:
    reveal = db.session.scalar(select(Spy.id).where(Spy.viewer_id == viewer_id, Spy.target_id == target_id))
    return reveal is not None

def add_reveal(viewer_id: int, target_id: int):
    reveal = Spy(viewer_id=viewer_id, target_id=target_id, reveal_date=today())
    db.session.add(reveal)
    return reveal