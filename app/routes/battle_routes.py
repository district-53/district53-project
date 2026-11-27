from flask import Blueprint, abort, render_template
from flask_login import login_required
from repositories import battle_repo, user_repo

battle_bp = Blueprint("battle", __name__)


@battle_bp.route("/battles/<int:battle_id>")
@login_required
def view_battle(battle_id):
    battle = battle_repo.get_battle(battle_id)
    if battle is None:
        abort(404)
    challenger = user_repo.get_user(battle.challenger_id)
    opponent = user_repo.get_user(battle.opponent_id)
    return render_template("battles/battle.html", battle=battle, challenger=challenger, opponent=opponent)