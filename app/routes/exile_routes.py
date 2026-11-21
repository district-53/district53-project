import hashlib
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from services.exile_service import is_exiled, to_exile

exile_bp = Blueprint("exile", __name__)


@exile_bp.before_app_request
def check_exile():
    if request.endpoint in ("exile.exile", "static"):
        return None

    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.headers.get("X-Real-IP") or request.remote_addr or ""

    ip_hash = hashlib.sha256(client_ip.encode("utf-8")).hexdigest()
    user_id = current_user.id if current_user.is_authenticated else None

    if is_exiled(user_id=user_id, ip_hashcode=ip_hash):
        return redirect(url_for("exile.exile"))

@exile_bp.route("/exile", methods=["GET"])
def exile():
    return render_template("exile.html")
    


@exile_bp.route("/exile/<int:target_id>", methods=["POST"])
@login_required
def exile_user(target_id):
    to_exile(user_id=target_id, exile_by=current_user.id)
    return redirect(url_for("book.book", kind="knight"))
