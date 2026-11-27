from extensions import db

from models.utils import today


class Spy(db.Model):
    __tablename__ = "reveals"

    id = db.Column(db.Integer, primary_key=True)
    viewer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reveal_date = db.Column(db.Date, default=today, nullable=False)