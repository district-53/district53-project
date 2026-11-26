from flask import Blueprint, Response, abort, jsonify, redirect, request, url_for
from flask_login import current_user, login_required

from errors import DomainError
from extensions import storage
from repositories import picture_repo, user_repo
from services import profile_service

picture_bp = Blueprint("pictures", __name__)


@picture_bp.route("/me/avatar", methods=["POST"])
@login_required
def upload_my_avatar():
    file = request.files.get("image")
    if file is None or file.filename == "":
        return jsonify(error="No file in the 'image' field"), 400

    try:
        picture = profile_service.change_avatar(current_user, file)
    except DomainError as error:
        return jsonify(error=error.message), 400

    return jsonify(picture_id=picture.id, url=url_for("pictures.get_picture", picture_id=picture.id)), 201


@picture_bp.route("/pictures/<int:picture_id>", methods=["GET"])
def get_picture(picture_id):
    picture = picture_repo.get_picture(picture_id)
    if picture is None or not storage.is_enabled:
        abort(404)

    data, content_type = storage.download(picture.s3_key)
    return Response(data, mimetype=content_type, headers={"Cache-Control": "public, max-age=31536000, immutable"})


@picture_bp.route("/users/<int:user_id>/avatar", methods=["GET"])
def get_user_avatar(user_id):
    user = user_repo.get_user(user_id)
    if user is None or user.photo_id is None:
        abort(404)
    return redirect(url_for("pictures.get_picture", picture_id=user.photo_id))