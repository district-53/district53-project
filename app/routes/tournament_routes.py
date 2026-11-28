from flask import Blueprint, render_template
from flask_login import login_required
from services import tournament_service

tournaments_bp = Blueprint("tournaments", __name__)

@tournaments_bp.route("/tournaments")
@login_required
def list_tournaments():
    items = tournament_service.get_tournaments()
    return render_template("tournaments/tournaments.html", tournaments=items)