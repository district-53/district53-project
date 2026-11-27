from extensions import db
from models.battles import Battle
from sqlalchemy import func, select


def create_battle(challenger_id, opponent_id, discipline):
    battle = Battle(
        challenger_id=challenger_id,
        opponent_id=opponent_id,
        discipline=discipline,
    )
    db.session.add(battle)
    db.session.flush()
    return battle


def get_battle(battle_id):
    return db.session.get(Battle, battle_id)


def has_pending_between(knight_a_id, knight_b_id):
    battles = db.session.scalar(
        select(func.count(Battle.id)).where(
            Battle.status == "pending",
            ((Battle.challenger_id == knight_a_id) & (Battle.opponent_id == knight_b_id))
            | ((Battle.challenger_id == knight_b_id) & (Battle.opponent_id == knight_a_id))
        )
    )
    return battles > 0