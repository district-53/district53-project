from extensions import db

from models.utils import now

NOTIFICATION_KINDS = ("house_request", "challenge", "tournament")


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    kind = db.Column(db.Enum(*NOTIFICATION_KINDS, name="notification_kind"), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=now, nullable=False)
