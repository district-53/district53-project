from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from services.exile_service import hash_ip, is_exiled, to_exile

exile_bp = Blueprint("exile", __name__)


@exile_bp.before_app_request
def check_exile():
    if request.endpoint in ("exile.exile", "static"):
        return None

    user = current_user if current_user.is_authenticated else None

    if is_exiled(user, hash_ip(request.remote_addr or "")):
        return redirect(url_for("exile.exile"))
    return None

@exile_bp.route("/exile", methods=["GET"])
def exile():
    return render_template("exile.html")
    


@exile_bp.route("/exile/<int:target_id>", methods=["POST"])
@login_required
def exile_user(target_id):
    try:
        to_exile(user_id=target_id, exile_by=current_user.id)
    except PermissionError:
        abort(403)
    return redirect(url_for("book.book", kind="knight", house=request.form.get("house", 0, type=int), spread=request.form.get("spread", 0, type=int)))
