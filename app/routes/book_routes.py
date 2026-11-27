from errors import DomainError
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from repositories import house_repo, user_repo
from services import battle_service, book_service, spy_service

book_bp = Blueprint("book", __name__)

@book_bp.route("/book")
@login_required
def book():
    kind, house = book_service.default_book(current_user, request.args.get("kind"), request.args.get("house", type=int))
    page = book_service.build_book(current_user, kind, house, spread=request.args.get("spread", type=int), focus=request.args.get("focus", type=int))

    gossip = None
    if current_user.role == "knight":
        gossip = spy_service.get_or_create_daily_gossip(current_user.id)

    return render_template("book/book.html", kind=kind, house=house, houses=house_repo.list_houses(), gossip=gossip, **page)

@book_bp.route("/book/reveal/<int:target_id>", methods=["POST"])
@login_required
def reveal_stats(target_id):
    entered_key = request.form.get("gossip_key", "").strip().upper()
    try:
        spy_service.use_gossip_key(current_user, target_id, entered_key)
    except DomainError as error:
        flash(error.message)
    return redirect(url_for("book.book", kind="knight", house=request.form.get("house", 0, type=int), spread=request.form.get("spread", 0, type=int)))


@book_bp.route("/book/challenge/<int:opponent_id>", methods=["POST"])
@login_required
def challenge(opponent_id):
    discipline = request.form.get("discipline", "")
    try:
        battle_service.challenge_knight(current_user, opponent_id, discipline)
        flash("Challenge sent")
    except DomainError as error:
        flash(error.message)
    return redirect(url_for("book.book", kind="knight", house=request.form.get("house", 0, type=int), spread=request.form.get("spread", 0, type=int)))


@book_bp.route("/search")
@login_required
def search():
    results = []
    for person in user_repo.search_people(request.args.get("q", "")):
        house = house_repo.get_house(person.house_id)
        results.append({
            "id": person.id,
            "name": person.username,
            "role": person.role,
            "house": house.name if house else None,
            "url": url_for("book.book", kind=person.role, house=0, focus=person.id),
        })
    return jsonify(results)