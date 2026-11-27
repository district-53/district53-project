from extensions import db

from models.utils import now


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    motto = db.Column(db.Text, nullable=False, default="")
    leader_id = db.Column(db.Integer, db.ForeignKey("knights.user_id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=now, nullable=False)
