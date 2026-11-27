from extensions import db

from models.utils import now

REQUEST_STATUSES = ("pending", "accepted", "declined")


class HouseRequest(db.Model):
    __tablename__ = "house_requests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)  # one request per user, ever
    house_id = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable=False)
    status = db.Column(db.Enum(*REQUEST_STATUSES, name="request_status"), default="pending", nullable=False)
    decided_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime(timezone=True), default=now, nullable=False)
    decided_at = db.Column(db.DateTime(timezone=True))
