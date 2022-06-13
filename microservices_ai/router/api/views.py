from quart import Blueprint, redirect
from quart_schema import hide_route


blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/")
@hide_route
async def index():
    return redirect("/docs")
