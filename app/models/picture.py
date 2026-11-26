from extensions import db
from models.utils import now

class Picture(db.Model):
    __tablename__ = "pictures"

    id = db.Column(db.Integer, primary_key=True)
    s3_key = db.Column(db.String(255), unique=True, nullable=False)
    size_bytes = db.Column(db.Integer, nullable=False)
    extension = db.Column(db.String(16), nullable=False)
    sha256_hash = db.Column(db.String(64), unique=True, nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id", use_alter=True, name="fk_pictures_uploaded_by"))
    created_at = db.Column(db.DateTime(timezone=True), default=now, nullable=False)