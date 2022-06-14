import os

import requests
import base64
from random import randint
from quart import (
    Blueprint, render_template,
    request, redirect, url_for,
)

blueprint = Blueprint("blueprint", __name__)


def make_request(url, data):
    return requests.post(url=url, json={"data": data}, headers={"Content-Type": "application/json"})


def counter(length=5):
    """Counter etc. 0001, 0002
    """
    number = '0' * length + str(randint(1, 9999))
    number = number[len(number)-length:]
    return number


def make_audio(data):
    sample = f"sample_{counter()}.wav"
    static = f"../static/samples/{sample}"
    folder = "frontend/static/samples/"
    samples = f"{folder}{sample}"
    with open(samples, mode="bx") as f:
        f.write(data)
    return static


url_stt = "http://127.0.0.1:5001/stt"
url_ai = "http://127.0.0.1:5002/ai"
url_tts = "http://127.0.0.1:5003/tts"


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

