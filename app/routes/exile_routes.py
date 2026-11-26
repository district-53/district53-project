from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from services import exile_service

exile_bp = Blueprint("exile", __name__)


@exile_bp.before_app_request
def check_exile():
    if request.endpoint in ("exile.exile", "static"):
        return None

    user = current_user if current_user.is_authenticated else None

    if exile_service.is_exiled(user, exile_service.hash_ip(request.remote_addr or "")):
        return redirect(url_for("exile.exile"))
    return None

@exile_bp.route("/exile", methods=["GET"])
def exile():
    return render_template("exile/exile.html")
    


@exile_bp.route("/exile/<int:target_id>", methods=["POST"])
@login_required
def exile_user(target_id):
    exile_service.to_exile(target_id=target_id, exiled_by=current_user)
    return redirect(url_for("book.book", kind="knight", house=request.form.get("house", 0, type=int), spread=request.form.get("spread", 0, type=int)))
