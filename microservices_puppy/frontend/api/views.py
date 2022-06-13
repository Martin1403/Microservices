import os
import requests
from flask import Blueprint, render_template, redirect, url_for, g

from frontend.api.forms import (
    AddForm, DelForm, GetForm, UpdateForm, AddOwnerForm
)


blueprint = Blueprint("frontend", __name__)
USER_API_URL = "http://puppy-service-c:5001/" \
    if os.environ.get("DOCKER") else "http://127.0.0.1:5001"


@blueprint.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@blueprint.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 500


@blueprint.route("/")
def home():
    return render_template("home.html")


@blueprint.route("/add", methods=["GET", "POST"])
def add_puppy():
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"name": name}
        response = requests.post(f"{USER_API_URL}/add", json=data, headers=headers)
        return redirect(url_for("frontend.list_puppies"))
    return render_template("add.html", form=form)


@blueprint.route("/list")
def list_puppies():
    headers = {"accept": "application/json"}
    response = requests.get(f"{USER_API_URL}/all", headers=headers)
    response = response.json()
    return render_template("list.html", puppies=response["puppies"])


@blueprint.route("/update", methods=["GET", "POST"])
def update_puppy():
    global g
    form1 = GetForm()
    form2 = UpdateForm()

    if form1.validate_on_submit() and not form2.name.data:
        headers = {"accept": "application/json"}
        id = form1.id.data
        g = id
        response = requests.get(f"{USER_API_URL}/puppy/{id}", headers=headers)
        response = response.json()
        form2.name.data = response.get("name")
        return render_template("update.html", form=form2)
    elif form2.name.data:
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        name = form2.name.data
        response = requests.put(f"{USER_API_URL}/puppy/{g}", json={"name": name}, headers=headers)
        return render_template("show.html", answer=name, id=g)

    return render_template("get.html", form=form1)


@blueprint.route("/get", methods=["GET", "POST"])
def get_puppy():
    form = GetForm()
    if form.validate_on_submit():
        id = form.id.data
        headers = {"accept": "application/json"}
        response = requests.get(f"{USER_API_URL}/puppy/{id}", headers=headers)
        response = response.json()
        answer = response.get("name") if response.get("name") else "No puppy found."
        owner = f'Owned by {response.get("owner")}' \
            if response.get("owner") else "Has no owner yet." if response.get("name") else ""
        return render_template("show.html", answer=answer, id=id, owner=owner)
    return render_template("get.html", form=form)


@blueprint.route("/delete", methods=["GET", "POST"])
def delete_puppy():
    form = DelForm()
    if form.validate_on_submit():
        id = form.id.data
        response = requests.delete(f"{USER_API_URL}/puppy/{id}")
        return redirect(url_for("frontend.list_puppies"))

    return render_template("delete.html", form=form)


@blueprint.route("/owner", methods=["POST", "GET"])
def add_owner():
    form = AddOwnerForm()
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"name": name, "puppy_id": id}
        response = requests.post(f"{USER_API_URL}/owner/", json=data, headers=headers)

        return redirect(url_for("frontend.list_puppies"))

    return render_template("owner.html", form=form)
