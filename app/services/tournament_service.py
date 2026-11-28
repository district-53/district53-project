from repositories import house_repo, tournament_repo, user_repo


def get_tournaments():
    tournaments = tournament_repo.list_tournaments()
    result = []
    for i in tournaments:
        result.append({
            "tournament": i,
            "host_house": house_repo.get_house(i.host_house_id),
            "winner": user_repo.get_user(i.winner_id) if i.winner_id else None,
        })
    return result