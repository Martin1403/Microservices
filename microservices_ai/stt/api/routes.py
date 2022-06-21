import os
import sys
import base64

from pydub import AudioSegment
from quart import Blueprint, redirect
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass

from stt.api.model import DeepSpeech

model_path = "stt/model/output_graph.tflite"
scorer_path = "stt/model/output_graph.scorer"
model = DeepSpeech(model_path=model_path if os.path.exists(model_path) else sys.exit(1),
                   scorer_path=scorer_path if os.path.exists(scorer_path) else None)



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
async def stt(data: DataSchema):
    """Speech to text.
    This function returns text from encoded wav data.
    """

    data = base64.decodebytes(data.data.encode('ascii'))
    audio_segment = AudioSegment(data, frame_rate=16000, sample_width=2, channels=1)
    np_audio = audio_segment[100:].get_array_of_samples()
    text = model.stt(np_audio)

    return {"data": text}
