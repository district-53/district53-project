from sqlalchemy import select

from extensions import db
from models.tournaments import Tournament


def get_tournament(tournament_id):
    return db.session.get(Tournament, tournament_id)


def list_tournaments():
    return db.session.scalars(select(Tournament).order_by(Tournament.starts_at)).all()
