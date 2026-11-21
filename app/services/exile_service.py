import string
from repositories.user_repo import update
from repositories.exile_repo import get_ips_by_id, block_ips, create_exile_record, get_blocked_ips_by_ip, get_blocked_ips_by_id
from repositories.user_repo import get_user
from repositories.knight_repo import get_knight




def to_exile(user_id: int, exile_by: int):
    lord = get_user(exile_by)
    target = get_user(user_id)
    knight = get_knight(user_id)

    if not lord or lord.role != "noble":
        raise PermissionError("Not allowed")
    if not target or not knight or lord.house_id is None or lord.house_id != target.house_id:
        raise PermissionError("Not allowed")

    ip_hashes = []
    for record in get_ips_by_id(user_id):
        ip_hashes.append(record.ip_hash)
    block_ips(user_id, ip_hashes)

    target = get_user(user_id)
    if target:
        update(target, is_exiled=True)

    create_exile_record(user_id=user_id, exile_by=exile_by)


def is_exiled(user_id: int | None, ip_hashcode: str) -> bool:
    if ip_hashcode and len(get_blocked_ips_by_ip(ip_hashcode)) > 0:
        return True
    if user_id is not None:
        user = get_user(user_id)
        if user and user.is_exiled:
            return True
        if len(get_blocked_ips_by_id(user_id)) > 0:
            return True
    return False

