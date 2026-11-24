from pathlib import Path
from werkzeug.datastructures import FileStorage
from extensions import db
from models import House, User
from repositories import user_repo
from repositories.picture_repo import save_picture, PictureError

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
    ("Ned Stark",        "Stark", "ned_stark.png"),
    ("Cersei Lannister", "Lannister", "cersei_lannister.png"),
    ("Olenna Tyrell",    "Tyrell", "olenna_tyrell.png"),
]

PORTRAITS_DIR = Path(__file__).resolve().parent / "portraits"
PORTRAITS = {
    **{username: photo for username, _, _, _, photo in KNIGHTS if photo},
    **{username: photo for username, _, photo in NOBLES if photo},
}

def add_houses():
    for name, motto in HOUSES:
        if not House.query.filter_by(name=name).first():
            db.session.add(House(name=name, motto=motto))
    db.session.commit()

def add_people():
    for username, house_name, stats, knight_type, _photo in KNIGHTS:
        if User.query.filter_by(username=username).first():
            continue
        house = House.query.filter_by(name=house_name).first()
        user_repo.create_user(
            username=username,
            email=username.lower().replace(" ", "_") + "@example.com",
            password=username.split()[-1].lower(),
            role="knight",
            house_id=house.id,
            stats={"strength": stats[0], "dexterity": stats[1], "constitution": stats[2]},
            knight_type=knight_type,
        )

    for username, house_name, _photo in NOBLES:
        if User.query.filter_by(username=username).first():
            continue
        house = House.query.filter_by(name=house_name).first()
        user_repo.create_user(
            username=username,
            email=username.lower().replace(" ", "_") + "@example.com",
            password=username.split()[-1].lower(),
            role="noble",
            house_id=house.id,
        )

def add_portraits():
    for username, filename in PORTRAITS.items():
        user = User.query.filter_by(username=username).first()
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
            except PictureError as error:
                print(f"[seed] skipped portrait for {username}: {error}")
                db.session.rollback()
                return

        user.photo_id = picture.id

    db.session.commit()


def seed():
    add_houses()
    add_people()
    add_portraits()