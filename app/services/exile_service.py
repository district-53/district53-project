import hmac
from flask import current_app
from errors import NotAllowed
from extensions import db
from models import User
from repositories import exile_repo, user_repo

def hash_ip(ip: str) -> str:
    key = current_app.config["SECRET_KEY"].encode()
    return hmac.new(key, ip.encode(), "sha256").hexdigest()


def can_exile(viewer: User, target: User) -> bool:
    return (viewer.role == "noble" and target.role == "knight" and target.house_id == viewer.house_id and not target.is_exiled)

def to_exile(target_id: int, exiled_by: User):
    target = user_repo.get_user(target_id)
    if target is not None and target.is_exiled:
        return
    if target is None or not can_exile(exiled_by, target):
        raise NotAllowed("NotAllowed")

    target.is_exiled = True
    exile_repo.create_exile_record(user_id=target_id, exiled_by=exiled_by)
    db.session.commit()


def is_exiled(user, ip_hash: str) -> bool:
    if user is not None and user.is_exiled:
        return True
    if current_app.config["EXILE_SWITCH"] and exile_repo.is_ip_blocked(ip_hash):
        return True
    return False

