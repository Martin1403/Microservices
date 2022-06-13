from quart import Blueprint, render_template
from ariadne import graphql
from ariadne.constants import PLAYGROUND_HTML
from quart import request, jsonify


from chat.api.schema import schema
from chat.app import app

blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/")
async def index():
    return await render_template("index.html")


@blueprint.route("/graphql", methods=["GET"])
async def graphql_playground():
    """supplies playground environment"""
    return PLAYGROUND_HTML, 200


@blueprint.route("/graphql", methods=["POST"])
async def graphql_server():
    data = await request.get_json()
    success, result = await graphql(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    return jsonify(result), 200 if success else 400
