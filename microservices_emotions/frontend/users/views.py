import os
from random import randint
import requests
from PIL import Image
from quart import Blueprint, render_template, request
from quart import flash, redirect, url_for
from flask_login import login_user, UserMixin, logout_user, \
    login_required, current_user
from werkzeug.utils import secure_filename

from .forms import RegistrationForm, LoginForm, UpdateUserForm

users = Blueprint("users", __name__)
url = "http://posts-service-c:5001/" if os.environ.get("DOCKER") else "http://127.0.0.1:5001"


class User(UserMixin):
    pass


@users.route("/register", methods=["GET", "POST"])
async def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        data = {"email": form.email.data, "username": form.username.data, "password": form.password.data}
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

        response = requests.request("POST", url=f"{url}/create", json=data, headers=headers)

        if response.status_code == 200:
            await flash("Thanks for registration!")
            return redirect(url_for("users.login"))
        elif response.status_code == 500:
            await flash("Email or username already registered!")
        else:
            raise NotImplemented(f"For {response.status_code}")
    return await render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
async def login():
    form = LoginForm()

    if form.validate_on_submit():
        data = {"email": form.email.data,  "password": form.password.data}
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        response = requests.request("POST", url=f"{url}/user", json=data, headers=headers)
        if response.status_code == 200:
            user = User()
            user.id = response.json().get("username")
            login_user(user)

            await flash("Log in Success.")

            n = request.args.get("next")
            if not n or not n[0] == "/":
                n = url_for("core.index")
            return redirect(n)

        elif response.status_code == 500:
            await flash(response.json().get("error"))
        else:
            raise NotImplemented(f"For {response.status_code}")

    return await render_template("login.html", form=form), 200


@users.route("/logout")
async def logout():
    logout_user()
    return redirect(url_for("core.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
async def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        # OBTAIN PICTURE FROM FORM AND SAVE IT.
        f = form.picture.data
        try:
            filename = secure_filename(f.filename)
            base = os.path.abspath(os.path.dirname(__name__))
            folder = os.path.join(base, "frontend", "static", "images")
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, filename)
            await f.save(path)
            # DELETE OLD, THUMBNAIL, RENAME AND SAVE.
            picture = Image.open(path)
            os.remove(path)
            picture.thumbnail((100, 100))
            i = randint(0, 100)
            picture_name = f"{current_user.id}_{i}.png"
            picture_path = os.path.join(folder, picture_name)
            [os.remove(f"{folder}/{i}") for i in os.listdir(folder) if i.startswith(current_user.id)]
            picture.save(picture_path)
        except AttributeError:
            picture_name = None

        response = requests.request("GET", url=f"{url}/user/{current_user.id}", headers={'accept': 'application/json'})
        user = response.json()

        data = {
            "username": current_user.id,
            "new_username": form.username.data,
            "new_email": form.email.data,
            "new_picture": picture_name if picture_name else user.get("profile_image")
        }

        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        response = requests.request("PUT", url=f"{url}/update", json=data, headers=headers)

        # IF USERNAME OR PASSWORD ARE CHANGED LOGOUT
        if form.username.data != user.get("username") or form.email.data != user.get("email"):
            logout_user()
            return redirect(url_for("core.index"))

        return await render_template("account.html", form=form, user=response.json())

    response = requests.request("GET", url=f"{url}/user/{current_user.id}", headers={'accept': 'application/json'})
    return await render_template("account.html", form=form, user=response.json())


@users.route("/<username>")
async def user_posts(username):
    user = requests.request("GET", url=f"{url}/user/{username}", headers={'accept': 'application/json'})
    response = requests.request("GET", url=f"{url}/post/{current_user.id}", headers={'accept': 'application/json'})
    blog_posts = response.json()
    return await render_template("posts.html", user=user.json(), blog_posts=blog_posts.get('posts'))
