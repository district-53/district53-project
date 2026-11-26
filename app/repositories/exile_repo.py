from extensions import db
from sqlalchemy import select
from models.user import User
from models.exiles import Exile
from models.user_ips import IP
from models.utils import now


def record_ip(user_id: int, ip_hash: str):
    record = db.session.scalar(select(IP).where(IP.user_id == user_id, IP.ip_hash == ip_hash))
    if record is None:
        db.session.add(IP(user_id=user_id, ip_hash=ip_hash))
    else:
        record.last_seen = now()

def create_exile_record(user_id: int, exiled_by: int, reason: str = "Exiled by lord") -> Exile:
    exile = Exile(user_id=user_id, exiled_by=exiled_by, reason=reason)
    db.session.add(exile)
    return exile


def is_ip_blocked(ip_hash: str) -> bool:
    query = db.session.scalar(
        select(IP.id)
        .join(User, User.id == IP.user_id)
        .where(IP.ip_hash == ip_hash, User.is_exiled.is_(True)))
    return query is not None