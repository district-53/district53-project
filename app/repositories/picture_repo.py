import hashlib

from errors import ValidationError
from extensions import db, storage
from models import Picture
from sqlalchemy import select
from storage import ALLOWED_IMAGE_TYPES


class PictureError(ValidationError):
    pass


def save_picture(file, uploaded_by=None):
    if not storage.is_enabled():
        raise PictureError("Photo upload is not available right now")
    if file.mimetype not in ALLOWED_IMAGE_TYPES:
        raise PictureError("Photo must be a JPG, PNG or WEBP image")

    data = file.read()
    if not data:
        raise PictureError("Photo file is empty")

    sha256 = hashlib.sha256(data).hexdigest()

    picture = db.session.scalar(select(Picture).where(Picture.sha256_hash == sha256))
    if picture is not None:
        return picture

    extension = ALLOWED_IMAGE_TYPES[file.mimetype]
    key = f"pictures/{sha256}.{extension}"
    storage.upload(data, key, file.mimetype)

    picture = Picture(
        s3_key=key,
        size_bytes=len(data),
        extension=extension,
        sha256_hash=sha256,
        uploaded_by=uploaded_by,
    )
    db.session.add(picture)
    db.session.flush()
    return picture

def get_picture(picture_id):
    return db.session.get(Picture, picture_id)