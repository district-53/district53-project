from extensions import db

ITEM_SLOTS = ("weapon", "armor", "shield", "helmet")


class Item(db.Model):
    __tablename__ = "items"
    __table_args__ = (
        db.CheckConstraint("str BETWEEN -20 AND 20", name="ck_item_str_mod"),
        db.CheckConstraint("dex BETWEEN -20 AND 20", name="ck_item_dex_mod"),
        db.CheckConstraint("con BETWEEN -20 AND 20", name="ck_item_con_mod"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    slot = db.Column(db.Enum(*ITEM_SLOTS, name="item_slot"), nullable=False)
    str = db.Column(db.Integer, default=0, nullable=False)
    dex = db.Column(db.Integer, default=0, nullable=False)
    con = db.Column(db.Integer, default=0, nullable=False)
    picture_id = db.Column(db.Integer, db.ForeignKey("pictures.id"))

    def get_mods(self) -> dict:
        return {
            "strength": self.str,
            "dexterity": self.dex,
            "constitution": self.con,
        }
