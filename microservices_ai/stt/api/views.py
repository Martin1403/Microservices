from quart import Blueprint, redirect
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass

from stt.api.actions import action_endpoint


blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/")
@hide_route
async def index():
    return redirect("/docs")


@dataclass
class DataSchema:
    """Encoded wav data."""
    data: str


@dataclass
class TextSchema:
    """Recognized text."""
    data: str


@blueprint.route("/stt", methods=["POST"])
@validate_request(DataSchema)
@validate_response(TextSchema)
@action_endpoint
async def stt(data: DataSchema):
    """Speech to text.
    This function returns text from encoded wav data.
    """
    return data
