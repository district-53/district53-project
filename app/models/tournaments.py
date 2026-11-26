from extensions import db
from models.utils import now

DISCIPLINES = ("joust", "melee", "archery")
TOURNAMENT_STATUSES = ("open", "running", "finished")


class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    discipline = db.Column(db.Enum(*DISCIPLINES, name="discipline"), nullable=False)
    host_house_id = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # a noble of the host house
    starts_at = db.Column(db.DateTime(timezone=True), nullable=False)
    status = db.Column(db.Enum(*TOURNAMENT_STATUSES, name="tournament_status"), default="open", nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey("knights.user_id"))
    created_at = db.Column(db.DateTime(timezone=True), default=now, nullable=False)


class TournamentEntry(db.Model):
    __tablename__ = "tournament_entries"
    __table_args__ = (
        db.UniqueConstraint("tournament_id", "knight_id", name="uq_tournament_entry"),
    )

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
    knight_id = db.Column(db.Integer, db.ForeignKey("knights.user_id"), nullable=False)
    joined_at = db.Column(db.DateTime(timezone=True), default=now, nullable=False)
