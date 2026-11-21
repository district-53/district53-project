from flask import Blueprint, flash, render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.exceptions import RequestEntityTooLarge
from models.user import User, load_user, ROLES
from models.houses import House
from extensions import db
from repositories import user_repo, picture_repo

auth_bp = Blueprint("auth", __name__)


STATS = ("strength", "dexterity", "constitution")
STAT_MIN, STAT_MAX = 1, 100

@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('book.book'))
    return render_template("index.html")

@auth_bp.route('/signup', defaults={'role': 'commonfolk'}, methods=['GET', 'POST'])
@auth_bp.route('/signup/<role>', methods=['GET', 'POST'])
def signup(role):
    if current_user.is_authenticated:
        return redirect(url_for('book.book'))

    if role not in ROLES:
        return redirect(url_for('auth.signup', role='commonfolk'))

    houses = House.query.order_by(House.name).all()
    if request.method == "GET":
        return render_template("signup.html", role=role, houses=houses, form={})
        
    if request.method == 'POST':
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get('password', "")

        existing = User.query.filter_by(username=username).first()
        if existing and existing.email == email:
            flash("You already have an account. Please log in.")
            return redirect(url_for("auth.login"))
        if existing:
            return render_template("signup.html", role=role, houses=houses, form={},
                                   error="Username already taken"), 400
        if User.query.filter_by(email=email).first():
            return render_template("signup.html", role=role, houses=houses, form={},
                                   error="Email already registered"), 400

        house_id = None
        if role in ("knight", "noble"):
            house_id = request.form.get("house_id", type=int)

        stats = None
        if role == "knight":
            stats = {name: request.form.get(name, type=int) for name in STATS}
            for name, value in stats.items():
                if value is None or not STAT_MIN <= value <= STAT_MAX:
                    return render_template("signup.html", role=role, houses=houses, form={},
                                        error=f"{name} must be between {STAT_MIN} and {STAT_MAX}"), 400

        photo = request.files.get("photo")
        has_photo = photo is not None and photo.filename != ""
        if role in ("knight", "noble") and not has_photo:
            return render_template("signup.html", role=role, houses=houses, form={},
                                error="Knights and nobles must upload a photo"), 400

        picture = None
        if has_photo:
            try:
                picture = picture_repo.save_picture(photo)
            except picture_repo.PictureError as e:
                db.session.rollback()
                return render_template("signup.html", role=role, houses=houses, form={},
                                    error=str(e)), 400

        user = user_repo.create_user(username, email, password, role, house_id=house_id,
                                    photo_id=picture.id if picture else None, stats=stats)

        if picture is not None and picture.uploaded_by is None:
            picture.uploaded_by = user.id
            db.session.commit()

    login_user(user)
    return redirect(url_for("book.book"))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('book.book'))

    if request.method == 'POST':
        username = request.form.get('username', "").strip()
        password = request.form.get('password', "")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('book.book'))
        flash("Wrong username or password")

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.app_errorhandler(RequestEntityTooLarge)
def file_too_large(e):
    if request.endpoint == "auth.signup":
        role = (request.view_args or {}).get("role") or "commonfolk"
        houses = House.query.order_by(House.name).all()
        return render_template("signup.html", role=role, houses=houses, form={},
                               error="Photo must be smaller than 5 MB"), 413
    return jsonify(error="File is too large (max 5 MB)"), 413
