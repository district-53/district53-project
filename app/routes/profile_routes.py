from errors import DomainError
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from models.knights import STAT_NAMES
from repositories import user_repo
from services import book_service, profile_service

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

@profile_bp.route("/<int:user_id>", methods=["GET"])
@login_required
def view_profile(user_id):
    user = user_repo.get_user(user_id)
    if user is None:
        abort(404)
    return render_template("book/profile.html", user=user, card=book_service.build_page(current_user, user))

@profile_bp.route("/<int:user_id>", methods=["POST"])
@login_required
def update_profile(user_id):
    if current_user.id != user_id:
        abort(403)
    photo = request.files.get("photo")
    try:
        profile_service.update_profile(
            current_user,
            username=request.form.get("username", "").strip(),
            email=request.form.get("email", "").strip().lower(),
            password=request.form.get("password", ""),
            stats={name: request.form.get(name, type=int) for name in STAT_NAMES},
            photo=photo if photo and photo.filename else None,
        )
        flash("Profile updated.")
    except DomainError as error:
        flash(error.message)

    return redirect(url_for("profile.view_profile", user_id=user_id))