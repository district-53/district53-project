import hmac
from flask import current_app
from extensions import db
from repositories.exile_repo import create_exile_record, is_ip_blocked
from repositories.knight_repo import get_knight
from repositories.user_repo import get_user

def hash_ip(ip: str) -> str:
    key = current_app.config["SECRET_KEY"].encode()
    return hmac.new(key, ip.encode(), "sha256").hexdigest()

def to_exile(user_id: int, exile_by: int):
    lord = get_user(exile_by)
    target = get_user(user_id)
    knight = get_knight(user_id)

    if not lord or lord.role != "noble" or lord.house_id is None:
        raise PermissionError("Not allowed")
    if not target or not knight or target.house_id != lord.house_id:
        raise PermissionError("Not allowed")
    if target.is_exiled:
        return

    target.is_exiled = True
    create_exile_record(user_id=user_id, exile_by=exile_by)
    db.session.commit()


def is_exiled(user, ip_hash: str) -> bool:
    if user is not None and user.is_exiled:
        return True
    if current_app.config["EXILE_SWITCH"] and is_ip_blocked(ip_hash):
        return True
    return False

