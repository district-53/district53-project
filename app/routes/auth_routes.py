from flask import Blueprint, flash, render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.exceptions import RequestEntityTooLarge

from errors import AlreadyRegistered, DomainError
from models.knights import STAT_NAMES
from models.user import ROLES
from repositories import house_repo
from services import auth_service

auth_bp = Blueprint("auth", __name__)

def _uploaded_photo(name: str):
    photo = request.files.get(name)
    return photo if photo is not None and photo.filename else None

@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('book.book'))
    return render_template("auth/index.html")

@auth_bp.route('/signup', defaults={'role': 'commonfolk'}, methods=['GET', 'POST'])
@auth_bp.route('/signup/<role>', methods=['GET', 'POST'])
def signup(role):
    if current_user.is_authenticated:
        return redirect(url_for('book.book'))
    if role not in ROLES:
        return redirect(url_for('auth.signup', role='commonfolk'))
    if request.method == "GET":
        return render_template("auth/signup.html", role=role, houses=house_repo.list_houses(), form=request.form, error=None)

    house_name = request.form.get("house_name", "").strip()
    house_motto = request.form.get("house_motto", "").strip()
    house_sigil = _uploaded_photo("house_sigil")
    is_new_house = bool(house_name or house_motto or house_sigil)

    try:
        user = auth_service.reg(
            role = role,
            username = request.form.get("username", "").strip(),
            email = request.form.get("email", "").strip().lower(),
            password = request.form.get('password', ""),
            house_id=request.form.get("house_id", type=int),
            is_new_house=is_new_house,
            name=house_name,
            motto=house_motto,
            sigil=house_sigil,
            stats = {name: request.form.get(name, type=int) for name in STAT_NAMES},
            photo = _uploaded_photo("photo"),
            ip = request.remote_addr or "",
        )
    except AlreadyRegistered as error:
        flash(error.message)
        return redirect(url_for("auth.login"))
    except DomainError as error:
        return render_template("auth/signup.html", role=role, houses=house_repo.list_houses(), form=request.form, error=error.message), 400

    login_user(user)
    return redirect(url_for("book.book"))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('book.book'))

    if request.method == 'POST':
        user = auth_service.auth(
            username = request.form.get('username', "").strip(),
            password = request.form.get('password', ""),
            ip = request.remote_addr or "",
        )

        if user is not None:
            login_user(user)
            return redirect(url_for('book.book'))
        flash("Wrong username or password")

    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.app_errorhandler(RequestEntityTooLarge)
def file_too_large(e):
    if request.endpoint == "auth.signup":
        role = (request.view_args or {}).get("role") or "commonfolk"
        return render_template("auth/signup.html", role=role, houses=house_repo.list_houses(), form=request.form, error="Photo must be smaller than 5 MB"), 413
    return jsonify(error="File is too large (max 5 MB)"), 413
