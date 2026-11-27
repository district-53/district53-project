from pathlib import Path

from errors import DomainError
from extensions import db
from models import House
from repositories import user_repo
from repositories.picture_repo import save_picture
from sqlalchemy import select
from werkzeug.datastructures import FileStorage

HOUSES = [
    ("Stark",     "Winter Is Coming"),
    ("Lannister", "Hear Me Roar!"),
    ("Targaryen", "Fire and Blood"),
    ("Baratheon", "Ours Is the Fury"),
    ("Tyrell",    "Growing Strong"),
    ("Mormont",   "Here We Stand"),
    ("Tarth",     ""),
    ("Selmy",     ""),
    ("Hedge Knights", "A knight's sword for hire"),
]

KNIGHTS = [
    ("Jaime Lannister",  "Lannister",     (88, 92, 80), "white",   "jaime_lannister.png"),
    ("Loras Tyrell",     "Tyrell",        (65, 88, 60), "regular", "loras_tyrell.png"),
    ("Brienne Tarth",    "Tarth",         (90, 70, 85), "regular", "brienne_tarth.png"),
    ("Jorah Mormont",    "Mormont",       (75, 65, 80), "regular", "jorah_mormont.png"),
    ("Jon Snow",         "Stark",         (82, 80, 86), "regular", "jon_snow.png"),
    ("Barristan Selmy",  "Selmy",         (78, 90, 70), "white",   "barristan_selmy.png"),
    ("Baelor Targaryen", "Targaryen",     (85, 78, 82), "regular", "baelor_targaryen.png"),
    ("Duncan the Tall",  "Hedge Knights", (95, 55, 92), "regular", "duncan_the_tall.png"),
    ("Daemon Targaryen", "Targaryen",     (84, 91, 74), "regular", "daemon_targaryen.png"),
]

NOBLES = [
    ("Ned Stark",        "Stark",   "ned_stark.png"),
    ("Cersei Lannister", "Lannister",   "cersei_lannister.png"),
    ("Olenna Tyrell",    "Tyrell",  "olenna_tyrell.png"),
]

PORTRAITS_DIR = Path(__file__).resolve().parent / "portraits"
PORTRAITS = {
    **{username: photo for username, _, _, _, photo in KNIGHTS if photo},
    **{username: photo for username, _, photo in NOBLES if photo},
}

def add_houses():
    existing = set(db.session.scalars(select(House.name)))
    for name, motto in HOUSES:
        if name not in existing:
            db.session.add(House(name=name, motto=motto))
    db.session.commit()

def add_people():
    houses = {house.name: house.id for house in db.session.scalars(select(House))}

    for username, house_name, (strength, dexterity, constitution), knight_type, _photo in KNIGHTS:
        if user_repo.username_taken(username):
            continue
        user_repo.create_user(
            username=username,
            email=username.lower().replace(" ", "_") + "@example.com",
            password=username.split()[-1].lower(),
            role="knight",
            house_id=houses[house_name],
            stats={"strength": strength, "dexterity": dexterity, "constitution": constitution},
            knight_type=knight_type,
        )

    for username, house_name, _photo in NOBLES:
        if user_repo.username_taken(username):
            continue
        user_repo.create_user(
            username=username,
            email=username.lower().replace(" ", "_") + "@example.com",
            password=username.split()[-1].lower(),
            role="noble",
            house_id=houses[house_name],
        )
    db.session.commit()

def add_portraits():
    for username, filename in PORTRAITS.items():
        user = user_repo.get_user_by_username(username)
        if user is None or user.photo_id:
            continue

        path = PORTRAITS_DIR / filename
        if not path.is_file():
            print(f"[seed] portrait missing for {username}: {path}")
            continue

        with path.open("rb") as stream:
            upload = FileStorage(stream=stream, filename=filename, content_type="image/png")
            try:
                picture = save_picture(upload, uploaded_by=user.id)
            except DomainError as error:
                print(f"[seed] skipped portrait for {username}: {error.message}")
                continue

        user.photo_id = picture.id
        db.session.commit()


def seed():
    add_houses()
    add_people()
    add_portraits()

