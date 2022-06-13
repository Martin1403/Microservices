from quart import Blueprint, render_template, redirect
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass

from chat.api.actions import action_endpoint

blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/")
@hide_route
async def index():
    return redirect("/docs")


@dataclass
class TextInSchema:
    data: str


@dataclass
class TextOutSchema:
    data: str


@blueprint.route("/post", methods=["POST"])
@validate_request(TextInSchema)
@validate_response(TextOutSchema)
@action_endpoint
async def post(data: TextInSchema):
    return data
