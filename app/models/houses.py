from extensions import db

from models.utils import now


class House(db.Model):
    __tablename__ = "houses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    motto = db.Column(db.Text, nullable=False, default="")
    sigil_id = db.Column(db.Integer, db.ForeignKey("pictures.id"))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id", use_alter=True, name="fk_houses_created_by"))
    created_at = db.Column(db.DateTime(timezone=True), default=now, nullable=False)
