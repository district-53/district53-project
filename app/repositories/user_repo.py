from extensions import db
from models import Knight, User

#write

def create_user(username, email, password, role, house_id=None, photo_id=None,
                stats=None, knight_type="regular"):

    user = User(username=username, email=email, role=role, house_id=house_id, photo_id=photo_id)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    if role == "knight":
        knight = Knight(user_id=user.id, knight_type=knight_type)
        knight.set_stats(stats["strength"], stats["dexterity"], stats["constitution"])
        db.session.add(knight)

    db.session.commit()
    return user


#read

def get_user(user_id):
    return db.session.get(User, user_id)


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def list_users(role=None):
    query = User.query
    if role is not None:
        query = query.filter_by(role=role)
    return query.order_by(User.username).all()


#update

def update(instance, **fields):
    for field_name, value in fields.items():
        setattr(instance, field_name, value)
    db.session.commit()