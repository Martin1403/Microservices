import os
from random import randint

import requests
from quart import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, UserMixin, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image

from frontend.api import url_for_chat, content_headers, save_user, get_user, get_logs, post_request
from frontend.api.measure.views import measure_endpoint
from frontend.api.base.forms import LoginForm, RegisterForm, UpdateForm
from frontend.api.chat.views import clear_chat
from frontend.api.base import (
    CREATE_USER_COMMAND,
    LOGIN_USER_COMMAND,
    UPDATE_USER_COMMAND,
    DELETE_USER_COMMAND
)

core = Blueprint("core", __name__)


async def save_picture(f):
    filename = secure_filename(f.filename)
    base = os.path.abspath(os.path.dirname(__name__))
    folder = os.path.join(base, "frontend", "static", "images")
    path = os.path.join(folder, filename)
    await f.save(path)
    picture = Image.open(path)
    os.remove(path)
    picture.thumbnail((50, 50))
    [os.remove(os.path.join(folder, i)) for i in os.listdir(folder) if i.startswith(get_user().get('username'))]
    picture_name = f"{get_user().get('username')}_{randint(0, 1000)}.png"
    picture_path = os.path.join(folder, picture_name)
    picture.save(picture_path)
    return picture_name


class User(UserMixin):
    def __repr__(self):
        return f"<User {self.__dict__}"


@core.route("/")
@measure_endpoint
async def home():
    return await render_template("index.html", page="home")


@core.route("/login", methods=["POST", "GET"])
@measure_endpoint
async def login():
    form = LoginForm()
    if form.validate_on_submit():
        query = LOGIN_USER_COMMAND.replace(
            "EMAIL", form.data["email"]).replace(
            "PASSWORD", form.data["password"])

        response = post_request(query=query)
        user = response.json().get('data').get('login')
        if user:
            user_login = User()
            user_login.id = user.get("id")
            login_user(user_login)
            save_user(user)
            return redirect(url_for("core.home", page="home", current_user=current_user))
    return await render_template("login.html", page="login", form=form)


@core.route("/register", methods=["POST", "GET"])
@measure_endpoint
async def register():
    form = RegisterForm()
    if form.validate_on_submit():
        credentials = {"username": form.data["username"],
                       "email": form.data["email"],
                       "password": form.data["password"]}
        response = post_request(query=CREATE_USER_COMMAND, input=credentials)
        if response.json().get('data').get('user'):
            return redirect(url_for("core.login"))
    return await render_template("register.html", page="register", form=form)


@core.route("/account", methods=["POST", "GET"])
@login_required
@measure_endpoint
async def account():
    form = UpdateForm()

    if request.method == "POST":
        if form.data.get("update"):
            f = form.picture.data
            response = post_request(
                query=UPDATE_USER_COMMAND,
                input=dict(
                    id=current_user.id,
                    email=form.data.get('email'),
                    new_username=form.data.get('username'),
                    password=form.data.get('password'),
                    picture=await save_picture(f)if f else None
                )

            )
            user = response.json().get('data').get('update')
            if user:
                save_user(user)

        elif form.data.get("delete"):
            query = DELETE_USER_COMMAND.replace("ID", current_user.id)
            response = post_request(query=query)
            return redirect(url_for("core.logout"))

    return await render_template("account.html", page="account", form=form, user=get_user())


@core.route("/logout", methods=["GET"])
@login_required
@measure_endpoint
async def logout():
    get_logs(reset=True)
    clear_chat()
    logout_user()
    return redirect(url_for("core.home", page="home"))
