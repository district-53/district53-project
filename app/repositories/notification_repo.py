from extensions import db
from models.notifications import Notification
from sqlalchemy import func, select, update


def create_notification(user_id, kind, text, link):
    notification = Notification(
        user_id=user_id,
        kind=kind,
        text=text,
        link=link,
    )
    db.session.add(notification)
    db.session.flush()
    return notification

def get_notification(notification_id):
    return db.session.get(Notification, notification_id)

def list_by_user(user_id):
    return db.session.scalars(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    ).all()

def count_unread(user_id):
    return db.session.scalar(
        select(func.count(Notification.id))
        .where(Notification.user_id == user_id, Notification.is_read.is_(False))
    )

def mark_all_as_read(user_id):
    db.session.execute(
        update(Notification)
        .where(Notification.user_id == user_id, Notification.is_read.is_(False))
        .values(is_read=True)
    )

def mark_as_read(notification: Notification):
    notification.is_read = True
