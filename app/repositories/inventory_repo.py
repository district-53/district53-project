from extensions import db
from sqlalchemy import select, delete
from models import Item, Knight, Equipment

def list_items():
    return db.session.scalars(select(Item).order_by(Item.name)).all()

def get_item(item_id):
    return db.session.get(Item, item_id)

def get_equipment(knight_id):
    return db.session.scalars(select(Equipment).where(Equipment.knight_id == knight_id)).all()

def get_slot(knight_id, slot):
    return db.session.get(Equipment, (knight_id, slot))

def equip(knight_id, slot, item_id):
    knight_slot = get_slot(knight_id, slot)
    if knight_slot is None:
        db.session.add(Equipment(knight_id=knight_id, slot=slot, item_id=item_id))
    else:
        knight_slot.item_id = item_id
    db.session.flush()

def unequip(knight_id, slot):
    db.session.execute(delete(Equipment).where(Equipment.knight_id == knight_id, Equipment.slot == slot))
