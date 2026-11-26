from extensions import db
from sqlalchemy import select
from models import House

def list_houses():
    return db.session.scalars(select(House).order_by(House.name)).all()

def get_house(house_id):
    return db.session.get(House, house_id)