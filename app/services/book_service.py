from models import User
from repositories import user_repo, knight_repo, house_repo
from services.exile_service import can_exile
from services.spy_service import can_reveal, can_see_stats

def build_page(viewer: User, person: User):
    """One page look"""
    house = house_repo.get_house(person.house_id)
    knight = knight_repo.get_knight(person.id) if person.role == "knight" else None
    stats = None
    if knight is not None and can_see_stats(viewer, knight, person.house_id):
        stats = knight.get_stats()
    return {
        "person": person,
        "house": house,
        "knight": knight,
        "stats": stats,
        "can_reveal": knight is not None and can_reveal(viewer, knight, stats is not None),
        "can_exile": can_exile(viewer, person),
    }

def build_book(viewer: User, kind: str, house: int, spread, focus):
    """Book and sidebar look"""
    names = user_repo.list_users(kind, house or None)
    ids = [row.id for row in names]

    if spread is None:
        target = focus if focus in ids else viewer.id
        if target in ids:
            spread = ids.index(target) // 2
        else:
            spread = 0

    if spread < 0:
        spread = 0

    first = spread * 2
    pages = [build_page(viewer, person) for person in user_repo.get_people(ids[first:first + 2])]

    return {
        "people": names, #sidebar
        "left": pages[0] if pages else None,
        "right": pages[1] if len(pages) > 1 else None,
        "spread": spread,
        "has_next": first + 2 < len(ids),
    }

def default_book(viewer: User, kind, house) -> tuple[str, int]:
    """Which book and which house to by defalt"""
    default_kind = "knight" if viewer.role == "knight" else "noble"
    if kind not in ("knight", "noble"):
        kind = default_kind
    if house is None:
        house = viewer.house_id if kind == "knight" and viewer.role == "noble" and viewer.house_id else 0
    return kind, house