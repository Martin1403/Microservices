from quart import Blueprint, render_template


error = Blueprint("error", __name__)


@error.app_errorhandler(404)
async def error404(_):
    return await render_template("404.html")


@error.app_errorhandler(405)
async def error405(_):
    return await render_template("405.html")


@error.app_errorhandler(500)
async def error500(_):
    return await render_template("500.html")
