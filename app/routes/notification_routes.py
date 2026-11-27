from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from services import notification_service


notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.app_context_processor
def show_unread_count():
    if current_user.is_authenticated:
        return {"unread_notifications": notification_service.get_unread_count(current_user.id)}
    return {"unread_notifications": 0}

@notifications_bp.route("/inbox")
@login_required
def inbox():
    items = notification_service.get_inbox(current_user.id)
    return render_template("book/inbox.html", notifications=items)


@notifications_bp.route("/inbox/<int:notification_id>/read", methods=["POST"])
@login_required
def mark_read(notification_id: int):
    notification_service.mark_read(notification_id, current_user.id)
    return redirect(url_for("book.inbox"))

@notifications_bp.route("/inbox/read-all", methods=["POST"])
@login_required
def mark_all_read():
    notification_service.mark_all_read(current_user.id)
    return redirect(url_for("book.inbox"))
