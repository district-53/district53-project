from flask import Blueprint, render_template

exile_bp = Blueprint("exile", __name__)


@exile_bp.route("/exile", methods=["GET"])
def exile():
    return render_template("exile.html")
    

