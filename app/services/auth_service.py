from errors import AlreadyRegistered, ValidationError
from extensions import db
from models import Knight, User
from models.user import ROLES
from repositories import exile_repo, house_repo, picture_repo, user_repo
from services.exile_service import hash_ip

def reg (*, role, username, email, password, house_id, stats, photo, ip) -> User:
    if role not in ROLES:
        raise ValidationError("Unknown role")
    if not username:
        raise ValidationError("Username is required")
    if not email:
        raise ValidationError("Email is required")

    existing = user_repo.get_user_by_username(username)
    if existing and existing.email == email:
        raise ValidationError("You already have an account")
    if existing:
        raise ValidationError("This username already taken")
    if user_repo.email_taken(email):
        raise ValidationError("This email already registered")

    if role in ("noble", "knight"):
        if house_id is None or house_repo.get_house(house_id) is None:
            raise ValidationError("Choose house")
        if photo is None:
            raise ValidationError("You must upload a portrait")
    else:
        house_id = None

    if role == "knight":
        Knight.validate_stats(stats)
    else:
        stats = None

    picture = None
    try:
        if photo is not None:
            picture = picture_repo.save_picture(photo)
        user = user_repo.create_user(username, email, password, role, house_id=house_id, photo_id=picture.id if picture else None, stats=stats)
        if picture is not None and picture.uploaded_by is None:
            picture.uploaded_by = user.id
        exile_repo.record_ip(user.id, hash_ip(ip))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise
    return user

def auth (username, password, ip) -> User | None:
    user = user_repo.get_user_by_username(username)
    if user is None or not user.check_password(password):
        return None
    exile_repo.record_ip(user.id, hash_ip(ip))
    db.session.commit()
    return user
