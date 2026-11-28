from errors import DomainError
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from services import inventory_service

inventory_bp = Blueprint("armory", __name__)


@inventory_bp.route("/armory")
@login_required
def armory():
    page = inventory_service.show_armory(current_user)
    return render_template("armory/armory.html", **page)


@inventory_bp.route("/armory/equip/<int:item_id>", methods=["POST"])
@login_required
def equip(item_id):
    try:
        item = inventory_service.equip(current_user, item_id)
        flash(f"{item.name} equipped")
    except DomainError as error:
        flash(error.message)
    return redirect(url_for("armory.armory"))


@inventory_bp.route("/armory/unequip/<slot>", methods=["POST"])
@login_required
def unequip(slot):
    try:
        inventory_service.unequip(current_user, slot)
        flash(f"{slot.capitalize()} removed")
    except DomainError as error:
        flash(error.message)
    return redirect(url_for("armory.armory"))