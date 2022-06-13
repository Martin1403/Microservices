from quart import Blueprint, render_template

from frontend.api import make_post_request
from frontend.api.users.forms import RegisterForm


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
async def chatbot():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        data.pop("submit")
        data.pop("csrf_token")
        assert data.get("password") == data.pop("pass_confirm")
        response = make_post_request(end="register", data={**data})
        # Response without error
        if response.status_code == 200:
            # Get text from stt response
            data = response.json().get("id")
            print("****DATA*****")
            print(data)
    return await render_template("register.html", form=form)
