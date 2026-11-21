from extensions import db
from sqlalchemy import or_
from models.exiles import Exile
from models.user_ips import IP
from models.utils import now


def create_exile_record(user_id: int, exile_by: int, reason: str = "Exiled by lord") -> Exile:
    exile = Exile(
        user_id=user_id,
        exile_by=exile_by,
        reason=reason,
        created_at=now(),
    )
    db.session.add(exile)
    db.session.commit()
    return exile


def get_ips_by_id(user_id: int) -> list[IP]:
    return IP.query.filter_by(user_id=user_id).all()


def block_ips(user_id: int, ip_hashes: list[str]):
    IP.query.filter(
        or_(IP.user_id == user_id, IP.ip_hash.in_(ip_hashes))
    ).update({"blocked": True}, synchronize_session=False)
    db.session.commit()


def get_blocked_ips_by_id(user_id: int) -> list[IP]:
    return IP.query.filter_by(user_id=user_id, blocked=True).all()


def get_blocked_ips_by_ip(ip_hash: str) -> list[IP]:
    return IP.query.filter_by(ip_hash=ip_hash, blocked=True).all()