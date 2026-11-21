from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models import House, Knight, User
from repositories.knight_repo import STAT_NAMES, can_see_stats, update_stats
from repositories.picture_repo import PictureError, save_picture

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

@profile_bp.route("/<int:user_id>", methods=["GET", "POST"])
@login_required
def view_profile(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == "POST":
        if current_user.id != user.id:
            abort(403)

        new_username = request.form.get("username", "").strip()
        new_email = request.form.get("email", "").strip().lower()
        new_password = request.form.get("password", "")

        if new_username != user.username and User.query.filter_by(username=new_username).first():
            flash("This username is already taken.")
            return redirect(url_for("profile.view_profile", user_id=user.id))

        if new_email != user.email and User.query.filter_by(email=new_email).first():
            flash("This email is already registered.")
            return redirect(url_for("profile.view_profile", user_id=user.id))

        knight = db.session.get(Knight, user.id) if user.role == "knight" else None
        if knight:
            stats = {name: request.form.get(name, type=int) for name in STAT_NAMES}
            try:
                update_stats(knight, stats)
            except ValueError as error:
                flash(str(error))
                return redirect(url_for("profile.view_profile", user_id=user.id))

        photo = request.files.get("photo")
        if photo and photo.filename:
            try:
                picture = save_picture(photo, uploaded_by=user.id)
            except PictureError as error:
                flash(str(error))
                return redirect(url_for("profile.view_profile", user_id=user.id))
            user.photo_id = picture.id

        user.username = new_username
        user.email = new_email
        if new_password:
            user.set_password(new_password)

        db.session.commit()
        flash("Profile updated.")
        return redirect(url_for("profile.view_profile", user_id=user.id))

    house = db.session.get(House, user.house_id) if user.house_id else None
    knight = db.session.get(Knight, user.id) if user.role == "knight" else None

    stats = None
    if knight and can_see_stats(current_user, knight):
        stats = knight.get_stats()

    return render_template("profile.html", user=user, house=house, knight=knight, stats=stats)