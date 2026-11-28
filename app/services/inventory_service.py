from errors import NotAllowed, NotFound, ValidationError
from extensions import db
from models.items import ITEM_SLOTS
from models.knights import STAT_NAMES
from repositories import inventory_repo, knight_repo


def get_knight(user):
    knight = knight_repo.get_knight(user.id) if user.role == "knight" else None
    if knight is None:
        raise NotAllowed("Only knights have an inventory")
    return knight

def get_slots(knight_id) -> dict:
    equipped = {slot: None for slot in ITEM_SLOTS}
    for row in inventory_repo.get_equipment(knight_id):
        equipped[row.slot] = inventory_repo.get_item(row.item_id)
    return equipped


def equip(user, item_id):
    knight = get_knight(user)
    item = inventory_repo.get_item(item_id)
    if item is None:
        raise NotFound("No such item in the armory")
    inventory_repo.equip(knight.user_id, item.slot, item.id)
    db.session.commit()
    return item


def unequip(user, slot):
    knight = get_knight(user)
    inventory_repo.unequip(knight.user_id, slot)
    db.session.commit()

def mod_stats(knight) -> dict:
    stats = knight.get_stats()
    for item in get_slots(knight.user_id).values():
        if item is None:
            continue
        for name, mod in item.get_mods().items():
            stats[name] += mod
    return {name: stats[name] for name in STAT_NAMES}


def show_armory(user) -> dict:
    knight = get_knight(user)
    catalogue = {slot: [] for slot in ITEM_SLOTS}
    for item in inventory_repo.list_items():
        catalogue[item.slot].append(item)

    return {
        "catalogue": catalogue,
        "equipped": get_slots(knight.user_id),
        "base_stats": knight.get_stats(),
        "stats": mod_stats(knight),
    }