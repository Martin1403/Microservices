import os

import requests
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, UserMixin, logout_user, \
    login_required, current_user

from frontend.api import url_for_users, content_headers
from frontend.api.users.forms import RegistrationForm, LoginForm

users = Blueprint("users", __name__)


class User(UserMixin):
    def __repr__(self):
        return f"<User {self.__dict__}"


@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        data = {"email": form.email.data, "username": form.username.data, "password": form.password.data}
        response = requests.request("POST", url=f"{url_for_users}/user", json=data, headers=content_headers)
        if response.status_code == 200:
            flash("Thanks for registration!")
            return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        data = {"email": form.email.data,  "password": form.password.data}
        response = requests.request("POST", url=f"{url_for_users}/check", json=data, headers=content_headers)
        if response.status_code == 200:
            user = response.json()

            user_login = User()
            user_login.id = user["user_id"]
            user_login.username = user["username"]
            user_login.email = user["email"]
            user_login.password = user["password"]

            login_user(user_login)
            flash("Log in Success.")

            return redirect(url_for("jobs.get_all_jobs"))

        elif response.status_code == 500:
            flash(response.json().get("error"))
        elif response.status_code == 404:
            flash(message="You are not registered.")
            return render_template("login.html", form=form), 200

    return render_template("login.html", form=form), 200


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.index"))