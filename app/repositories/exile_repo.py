from extensions import db
from models.user import User
from models.exiles import Exile
from models.user_ips import IP
from models.utils import now


def record_ip(user_id: int, ip_hash: str):
    record = IP.query.filter_by(user_id=user_id, ip_hash=ip_hash).first()
    if record is None:
        db.session.add(IP(user_id=user_id, ip_hash=ip_hash))
    else:
        record.last_seen = now()

def create_exile_record(user_id: int, exile_by: int, reason: str = "Exiled by lord") -> Exile:
    exile = Exile(
        user_id=user_id,
        exile_by=exile_by,
        reason=reason,
        created_at=now(),
    )
    db.session.add(exile)
    return exile


def is_ip_blocked(ip_hash: str) -> bool:
    return (IP.query.join(User, User.id == IP.user_id)
            .filter(IP.ip_hash == ip_hash, User.is_exiled.is_(True))
            .first() is not None)