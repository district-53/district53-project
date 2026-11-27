from errors import ValidationError
from extensions import db
from models.notifications import NOTIFICATION_KINDS
from repositories import notification_repo

def create(user_id, kind, text, link):
    if kind not in NOTIFICATION_KINDS:
        raise ValidationError("Unknown kind")
    text = text.strip()
    if not text:
        raise ValidationError("Notification text cannot be empty")
    return notification_repo.create_notification(user_id=user_id, kind=kind, text=text, link=link)

def get_inbox(user_id):
    return notification_repo.list_by_user(user_id)

def get_unread_count(user_id):
    return notification_repo.count_unread(user_id)

def mark_read(notification_id, user_id):
    notification = notification_repo.get_notification(notification_id)
    if notification is None or notification.user_id != user_id:
        raise ValidationError("Notification not found")
    if not notification.is_read:
        notification_repo.mark_as_read(notification)
        db.session.commit()

def mark_all_read(user_id):
    notification_repo.mark_all_as_read(user_id)
    db.session.commit()