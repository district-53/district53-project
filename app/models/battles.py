from extensions import db

from models.tournaments import DISCIPLINES
from models.utils import now

BATTLE_STATUSES = ("pending", "accepted", "declined", "finished")


class Battle(db.Model):
    __tablename__ = "battles"
    __table_args__ = (
        db.CheckConstraint("challenger_id <> opponent_id", name="ck_battle_not_self"),
    )

    id = db.Column(db.Integer, primary_key=True)
    challenger_id = db.Column(db.Integer, db.ForeignKey("knights.user_id"), nullable=False)
    opponent_id = db.Column(db.Integer, db.ForeignKey("knights.user_id"), nullable=False)
    discipline = db.Column(db.Enum(*DISCIPLINES, name="discipline"), nullable=False)
    status = db.Column(db.Enum(*BATTLE_STATUSES, name="battle_status"), default="pending", nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"))
    winner_id = db.Column(db.Integer, db.ForeignKey("knights.user_id"))
    created_at = db.Column(db.DateTime(timezone=True), default=now, nullable=False)
    finished_at = db.Column(db.DateTime(timezone=True))


class BattleRound(db.Model):
    __tablename__ = "battle_rounds"
    __table_args__ = (
        db.UniqueConstraint("battle_id", "round_no", name="uq_battle_round"),
    )

    id = db.Column(db.Integer, primary_key=True)
    battle_id = db.Column(db.Integer, db.ForeignKey("battles.id"), nullable=False)
    round_no = db.Column(db.Integer, nullable=False)
    challenger_roll = db.Column(db.Integer, nullable=False)
    opponent_roll = db.Column(db.Integer, nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey("knights.user_id"))
