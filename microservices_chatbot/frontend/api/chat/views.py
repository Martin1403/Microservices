from datetime import datetime

import requests
from quart import Blueprint, render_template, redirect, url_for

from frontend.api import get_user
from frontend.api.measure.views import measure_endpoint
from flask_login import login_required, current_user

from frontend.api.chat.forms import ChatForm
from frontend.api import url_for_ai, post_request
from frontend.api.chat import CREATE_POST_COMMAND

chats = Blueprint("chats", __name__)

responses = []


def clear_chat():
    global responses
    responses.clear()
    responses = []


@chats.route("/chat", methods=["POST", "GET"])
@login_required
@measure_endpoint
async def chat():
    global responses
    form = ChatForm()
    if form.validate_on_submit():
        reset_memory = 10 if len(responses) % 10 == 0 else 0
        user_text = form.data.get("text")
        user_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = requests.request(
            method="POST",
            url=f"{url_for_ai}/chat",
            json={
                "input": user_text,
                "input_date": user_date,
                "reset": reset_memory,
            }
        )
        response = response.json()
        responses.append(response)

        response = post_request(
            query=CREATE_POST_COMMAND,
            input=dict(
                user_id=current_user.id,
                user_text=user_text,
                user_date=user_date,
                ai_text=response.get('output'),
                ai_date=response.get('output_date')

            )

        )

        return redirect(url_for('chats.chat'))
    return await render_template("chat.html", page="chat", form=form, data=responses, user=get_user())


@chats.route("/reset", methods=['POST', "GET"])
async def reset():
    global responses
    responses.clear()
    return redirect(url_for('chats.chat'))
