from extensions import db
from models import Knight, User
from sqlalchemy import select


#write

def create_user(username, email, password, role, house_id=None, photo_id=None, stats=None, knight_type="regular"):

    user = User(username=username, email=email, role=role, house_id=house_id, photo_id=photo_id)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    if role == "knight":
        knight = Knight(user_id=user.id, knight_type=knight_type)
        knight.set_stats(stats)
        db.session.add(knight)
    return user


#read

def get_user(user_id):
    return db.session.get(User, user_id)


def get_user_by_username(username):
    return db.session.scalar(select(User).where(User.username == username))

def username_taken(username: str) -> bool:
    return get_user_by_username(username) is not None

def email_taken(email: str) -> bool:
    return db.session.scalar(select(User.id).where(User.email == email)) is not None


def list_users(role=None, house_id=None):
    """For sidebar"""
    query = select(User.id, User.username).where(User.role == role)
    if house_id is not None:
        query = query.where(User.house_id == house_id)
    return db.session.execute(query.order_by(User.username)).all()


def get_people(user_ids: list[int]):
    """For book"""
    if not user_ids:
        return []
    users = db.session.scalars(select(User).where(User.id.in_(user_ids))).all()

    by_id = {user.id: user for user in users}
    result = []
    for user_id in user_ids:
        if user_id in by_id:
            result.append(by_id[user_id])
    return result
    

def search_people(text, limit=10):
    text = (text or "").strip()
    if not text:
        return []

    safe = text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    pattern = f"%{safe}%"

    query = (
        select(User)
        .where(User.role.in_(("knight", "noble")), User.username.ilike(pattern, escape="\\"))
        .order_by(User.username)
        .limit(limit)
    )
    return db.session.scalars(query).all()