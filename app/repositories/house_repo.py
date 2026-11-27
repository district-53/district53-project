from extensions import db
from models import House
from sqlalchemy import select


def list_houses():
    return db.session.scalars(select(House).order_by(House.name)).all()

def get_house(house_id):
    return db.session.get(House, house_id)

def create_house(name, motto, sigil_id=None):
    house = House(name=name, motto=motto, sigil_id=sigil_id)
    db.session.add(house)
    db.session.flush()
    return house

def house_name_taken(name):
    return db.session.scalar(select(House.id).where(House.name == name)) is not None