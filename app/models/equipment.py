from extensions import db

from models.items import ITEM_SLOTS


class Equipment(db.Model):
    __tablename__ = "equipment"

    knight_id = db.Column(db.Integer, db.ForeignKey("knights.user_id"), primary_key=True)
    slot = db.Column(db.Enum(*ITEM_SLOTS, name="item_slot"), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
