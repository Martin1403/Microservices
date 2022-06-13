import os

from pydantic.dataclasses import dataclass
from quart import Blueprint, render_template
from quart_schema import validate_request, validate_response

from .model import Emotions

blueprint = Blueprint("blueprint", __name__)

base = os.path.abspath(os.path.dirname(__name__))
data_folder = os.path.join(base, "emotions/data")
emotion = Emotions(path=data_folder)


@blueprint.route("/")
async def home():
    """Home page.
    Rendering home page.
    """
    return await render_template("index.html")


@blueprint.before_app_serving
def load_data():
    emotion.load_model()


@dataclass
class TextSchema:
    text: str


@dataclass
class EmotionSchema(TextSchema):
    emotion: str


@blueprint.route("/emotions", methods=["POST"])
@validate_request(TextSchema)
@validate_response(EmotionSchema, status_code=200)
def get_emotion(data: TextSchema):
    """Get emotion.
    The function returns emotion from text.
    """
    text = data.text
    return EmotionSchema(text=text, emotion=emotion.get_emotion(text))
