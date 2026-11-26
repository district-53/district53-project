from extensions import db
from errors import ValidationError

KNIGHT_TYPES = ("regular", "white")
STAT_NAMES = ("strength", "dexterity", "constitution")

class Knight(db.Model):
    __tablename__ = "knights"
    __table_args__ = (
        db.CheckConstraint("strength BETWEEN 1 AND 100", name="ck_knight_strength"),
        db.CheckConstraint("dexterity BETWEEN 1 AND 100", name="ck_knight_dexterity"),
        db.CheckConstraint("constitution BETWEEN 1 AND 100", name="ck_knight_constitution"),
    )

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    knight_type = db.Column(db.Enum(*KNIGHT_TYPES, name="knight_type"), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    gossip_key = db.Column(db.String(255), unique=True)
    key_date = db.Column(db.Date)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id", use_alter=True, name="fk_knights_company_id"))

    @staticmethod
    def validate_stats(stats: dict):
        for name in STAT_NAMES:
            value = stats.get(name)
            if not isinstance(value, int) or isinstance(value, bool) or not (1 <= value <= 100):
                raise ValidationError(f"{name} must be an integer from 1 to 100.")
        
    def set_stats(self, stats: dict):
        self.validate_stats(stats)
        self.strength = stats.get("strength")
        self.dexterity = stats.get("dexterity")
        self.constitution = stats.get("constitution")


    def get_stats(self) -> dict:
        return {
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
        }
    