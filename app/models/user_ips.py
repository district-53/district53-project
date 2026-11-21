from extensions import db
from models.utils import now

class IP(db.Model):
    __tablename__ = "user_ips"
    __table_args__ = (db.UniqueConstraint("user_id", "ip_hash"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ip_hash = db.Column(db.String(255), nullable=False)
    first_seen = db.Column(db.DateTime(timezone=True), default=now, nullable=False)
    last_seen = db.Column(db.DateTime(timezone=True), default=now, nullable=False)