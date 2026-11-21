import hashlib

import storage
from extensions import db
from models.picture import Picture


class PictureError(ValueError):
    pass


def save_picture(file, uploaded_by=None):
    if not storage.is_enabled():
        raise PictureError("Photo upload is not available right now")
    if file.mimetype not in storage.ALLOWED_IMAGE_TYPES:
        raise PictureError("Photo must be a JPG, PNG or WEBP image")

    data = file.read()
    if not data:
        raise PictureError("Photo file is empty")

    sha256 = hashlib.sha256(data).hexdigest()

    picture = Picture.query.filter_by(sha256_hash=sha256).first()
    if picture is not None:
        return picture

    extension = storage.ALLOWED_IMAGE_TYPES[file.mimetype]
    key = f"pictures/{sha256}.{extension}"
    storage.upload_bytes(data, key, file.mimetype)

    picture = Picture(
        seaweed_fid=key,
        size_bytes=len(data),
        extension=extension,
        sha256_hash=sha256,
        uploaded_by=uploaded_by,
    )
    db.session.add(picture)
    db.session.flush()
    return picture