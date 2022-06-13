from quart import Blueprint, render_template, request


error = Blueprint("error", __name__)


@error.app_errorhandler(404)
async def error404(e):
    return await render_template("404.html"), 404
