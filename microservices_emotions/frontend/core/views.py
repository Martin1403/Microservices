from quart import Blueprint, render_template
from flask_login import current_user

core = Blueprint("core", __name__)


@core.route("/")
async def index():
    return await render_template("index.html", current_user=current_user)

