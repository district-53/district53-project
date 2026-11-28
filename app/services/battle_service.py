from errors import ValidationError
from extensions import db
from models.tournaments import DISCIPLINES
from repositories import battle_repo, knight_repo, user_repo
from services import notification_service


def can_challenge(viewer, target):
    if viewer.role != "knight" or target.role != "knight":
        return False
    if viewer.id == target.id:
        return False
    if viewer.house_id == target.house_id:
        return False
    return not battle_repo.has_pending_between(viewer.id, target.id)


def challenge_knight(challenger, opponent_id, discipline):
    if discipline not in DISCIPLINES:
        raise ValidationError("Unknown discipline")

    opponent = user_repo.get_user(opponent_id)
    if (opponent is None or knight_repo.get_knight(challenger.id) is None or knight_repo.get_knight(opponent.id) is None or not can_challenge(challenger, opponent)):
        raise ValidationError("You cannot challenge this knight")
    
    battle = battle_repo.create_battle(
        challenger_id=challenger.id,
        opponent_id=opponent.id,
        discipline=discipline,
    )
    notification_service.create(
        user_id=opponent.id,
        kind="challenge",
        text=f"{challenger.username} challenged you to a {discipline} duel!",
        link=f"/battles/{battle.id}"
    )
    notification_service.create(
        user_id=challenger.id,
        kind="challenge",
        text=f"You challenged {opponent.username} to a {discipline} duel!",
        link=f"/battles/{battle.id}",
    )
    db.session.commit()
    return battle