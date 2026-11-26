from errors import ValidationError
from extensions import db
from models import User
from repositories import picture_repo, user_repo, knight_repo


def update_profile(user: User, *, username, email, password, stats, photo):
    if username != user.username and user_repo.username_taken(username):
        raise ValidationError("This username is already taken.")
    if email != user.email and user_repo.email_taken(email):
        raise ValidationError("This email is already registered.")

    knight = knight_repo.get_knight(user.id)
    if knight is not None:
        knight.validate_stats(stats)

    picture = None
    try:
        if photo is not None:
            picture = picture_repo.save_picture(photo)
            user.photo_id = picture.id
        if knight:
            knight.set_stats(stats)
        user.username = username
        user.email = email
        if password:
            user.set_password(password)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

def change_avatar(user: User, photo):
    picture = None
    try:
        picture = picture_repo.save_picture(photo)
        user.photo_id = picture.id
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return picture
