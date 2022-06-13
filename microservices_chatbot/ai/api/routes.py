import re
import datetime
from typing import Tuple, Union

from quart import Blueprint, render_template
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass

from ai.api.achat import ChatBot

blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/")
@hide_route
async def home():
    return await render_template("index.html")


@dataclass
class TextSchema:
    """Input text and reset memory"""
    input: str
    input_date: str
    reset: int


@dataclass
class ChatSchema(TextSchema):
    """Api output"""
    output: str
    output_date: str


@dataclass
class ErrorSchema:
    error: str


def text_filter(text):
    text = re.sub(r"\$", "", text)
    return text.capitalize()


@blueprint.route("/chat", methods=["POST"])
@validate_request(TextSchema)
@validate_response(ChatSchema)
@validate_response(ErrorSchema, status_code=400)
async def get_chat(data: TextSchema) -> Tuple[Union[ChatSchema, ErrorSchema], int]:
    """Get answer.
    Function return answer from chatbot.
    """
    async with ChatBot(text=data.input) as model:
        model = await model
    try:
        response = ChatSchema(
            input=data.input,
            input_date=data.input_date,
            reset=int(data.reset),
            output=text_filter(model.output),
            output_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return response, 200
    except ValueError:
        return ErrorSchema("Something...."), 400
