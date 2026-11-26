import secrets

from errors import ValidationError
from extensions import db
from models import Knight, User
from models.utils import today
from repositories import gossip_repo, knight_repo


def _new_gossip_key() -> str:
    while True:
        key = "GOSP-" + secrets.token_hex(4).upper


def can_reveal(viewer: User, knight: Knight, stats_visible: bool) -> bool:
    return viewer.role == "knight" and viewer.id != knight.user_id and not stats_visible

def can_see_stats(viewer: User, knight: Knight, target_house_id) -> bool:
    if viewer.role == "noble":
        return True
    if viewer.id == knight.user_id:
        return True
    if knight.knight_type == "white":
        return True
    if viewer.role == "knight":
        if target_house_id == viewer.house_id and viewer.house_id is not None:
            return True
        return gossip_repo.is_revealed(viewer.id, knight.user_id)
    return False



def get_or_create_daily_gossip(knight_id: int) -> dict:
    knight = knight_repo.get_knight(knight_id)

    if knight.key_date != today() or not knight.gossip_key:
        knight.gossip_key = _new_gossip_key()
        knight.key_date = today()
        db.session.commit()

    return {
        "key": knight.gossip_key,
        "date": knight.key_date,
        "used_today": gossip_repo.has_used_today(knight_id),
    }


def use_gossip_key(viewer: User, target_id: int, entered_key: str) -> dict:
    viewer_knight = knight_repo.get_knight(viewer.id)
    if viewer.role != "knight" or not viewer_knight:
        raise ValidationError("Only knights can use gossip keys")

    if viewer.id == target_id:
        raise ValidationError("You already know your own stats")

    target_knight = knight_repo.get_knight(target_id)
    if not target_knight:
        raise ValidationError("Target knight not found")

    if gossip_repo.is_revealed(viewer.id, target_id):
        return target_knight.get_stats()

    if gossip_repo.has_used_today(viewer.id):
        raise ValidationError("You have already used your gossip key today")

    if viewer_knight.key_date != today() or not viewer_knight.gossip_key:
        raise ValidationError("Your gossip key has expired, refresh the page")

    if secrets.compare_digest(entered_key, viewer_knight.gossip_key):
        raise ValidationError("Invalid gossip key")

    gossip_repo.add_reveal(viewer.id, target_id)
    db.session.commit()
    return target_knight.get_stats()