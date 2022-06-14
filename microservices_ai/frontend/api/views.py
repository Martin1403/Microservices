import os
import uuid
import requests
import base64
from random import randint
from quart import (
    Blueprint, render_template,
    request, redirect, url_for,
)

blueprint = Blueprint("blueprint", __name__)
base = os.path.abspath(os.path.dirname(__name__))


def make_request(url, data):
    return requests.post(url=url, json={"data": data}, headers={"Content-Type": "application/json"})


def make_audio(data):

    sample = f"{uuid.uuid4()}.wav"
    static = f"../static/samples/{sample}"
    folder = os.path.join(base, "frontend/static/samples")
    samples = os.path.join(folder, sample)
    with open(samples, mode="bx") as f:
        f.write(data)
    return static


url_stt = "http://127.0.0.1:5001/stt"
url_ai = "http://127.0.0.1:5002/ai"
url_tts = "http://127.0.0.1:5003/tts"

if os.environ.get("DOCKER"):
    url_stt = "http://stt-service-c:5001/stt"
    url_ai = "http://ai-service-c:5002/ai"
    url_tts = "http://tts-service-c:5003/tts"


@blueprint.route("/", methods=["GET", "POST"])
async def index():

    if request.method == "POST":
        data = await request.get_data()                             # WEB => WAV
        data = base64.encodebytes(data).decode('ascii')             # BYTES => STR
        response = make_request(url=url_stt, data=data)             # STR => STT
        user_text = response.json().get("data")                     # STT => TEXT
        response = make_request(url=url_ai, data=user_text)         # TEXT => AI
        ai_text = response.json().get("data")[:-1]                  # AI => TEXT
        response = make_request(url=url_tts, data=ai_text)          # TEXT => TTS
        data = response.json().get("data")                          # TTS => STR
        data = base64.decodebytes(data.encode('ascii'))             # STR => BYTES
        static = make_audio(data)                                   # BYTES => WAV
        return {"user": user_text, "ai": ai_text, "path": static}   # DATA => WEB

    return await render_template("index.html")

