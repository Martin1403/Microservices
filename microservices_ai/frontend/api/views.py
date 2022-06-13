import base64
import logging
import os
from random import randint
import numpy as np
import requests
from scipy.io.wavfile import write
from quart import Blueprint, render_template, request, redirect, url_for


blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/")
async def index():
    return await render_template("index.html")


@blueprint.route("/chatbot", methods=["GET", "POST"])
async def chatbot():
    [os.remove(f"frontend/static/{i}") for i in os.listdir("frontend/static/") if i.endswith(".wav")]
    if request.method == "POST":
        # Wav data (bytes)
        data = await request.get_data()
        # Make request to router.
        response = requests.post(
            url="http://router-service-c:5001/router" if os.environ.get("DOCKER") else "http://127.0.0.1:5001/router",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={"data":  base64.encodebytes(data).decode('ascii'),  # Decode data to string
                  },
        )
        # Response without error
        if response.status_code == 200:
            # Get text from stt response
            data = response.json().get("data")
            print("****DATA*****")
            print(data)
    return await render_template("chatbot.html")


"""TEXT TO TTS
# Make request to tts (send text and get list of floats)
response = make_request(url=urls["tts"], data=text)
if response.status_code == 200:
    response = response.json()
    # Rate 22050, data list of floats
    rate, data = response.get("rate"), response.get("data")
    data = base64.decodebytes(data.encode('ascii'))
    path = f"/static/test_{randint(0, 200)}.wav"
    # Convert list to array and write wav
    with open(f"frontend{path}", mode='bx') as f:
        f.write(data)
    # write(f"frontend{path}", rate=rate, data=data)
    # Send data back to page
    return {"user": text, "bot": "Not here", "audio": f"..{path}"}
"""