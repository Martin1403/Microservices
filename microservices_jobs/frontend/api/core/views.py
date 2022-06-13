from flask import Blueprint, render_template
from flask_login import current_user

core = Blueprint("core", __name__)


@core.route("/")
def index():
    return render_template("index.html", current_user=current_user)
