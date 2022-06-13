import os
import ast
import datetime

import json
import requests
from quart import Blueprint, render_template, request
from quart import flash, redirect, url_for
from flask_login import login_user, UserMixin, logout_user, \
    login_required, current_user
from werkzeug.utils import secure_filename

from .forms import BlogPostForm, UpdateBlogPostForm

posts = Blueprint("posts", __name__)
url = "http://posts-service-c:5001/" if os.environ.get("DOCKER") else "http://127.0.0.1:5001"


@posts.route("/create", methods=["POST", "GET"])
@login_required
async def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        data = {"username": current_user.id, "title": form.title.data, "text": form.text.data}
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

        blog_post = requests.request("POST", url=f"{url}/post/create", json=data, headers=headers)

        user = requests.request("GET", url=f"{url}/user/{current_user.id}", headers={'accept': 'application/json'})

        response = requests.request("GET", url=f"{url}/post/{current_user.id}", headers={'accept': 'application/json'})
        blog_posts = response.json()

        return await render_template("posts.html", user=user.json(), blog_posts=blog_posts.get('posts'))

    response = requests.request("GET", url=f"{url}/user/{current_user.id}", headers={'accept': 'application/json'})
    return await render_template("post.html", form=form, user=response.json())


@posts.route("/update", methods=["POST", "GET"])
@login_required
async def update_post():
    """Update or delete post by post id"""
    post, user = request.args.get("post"), request.args.get("user")
    post, user = ast.literal_eval(post), ast.literal_eval(user)

    form = UpdateBlogPostForm()
    form.id.data = post.get("id")
    form.id.label = f"id: {post.get('id')}"
    form.title.render_kw["placeholder"] = post.get("title")
    form.text.render_kw["placeholder"] = post.get("text")
    if request.method == "POST":
        response = await request.form
        # FOR UPDATE POST
        if response.get("update"):
            if form.id.data and form.title.data:
                data = {"id": form.id.data, "title": form.title.data, "text": form.text.data}
                headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
                response = requests.request("PUT", url=f"{url}/post/update", json=data, headers=headers)
        # FOR DELETE POST
        elif response.get("delete"):
            data = {"id": form.id.data}
            headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
            response = requests.request("DELETE", url=f"{url}/post/delete", json=data, headers=headers)
            if response.status_code == 204:
                await flash("Deleted")
        else:
            raise NotImplemented("Not implemented yet.")

        response = requests.request("GET", url=f"{url}/post/{current_user.id}", headers={'accept': 'application/json'})
        blog_posts = response.json()
        return await render_template("posts.html", user=user, blog_posts=blog_posts.get('posts'))

    return await render_template("update.html", form=form, user=user)


@posts.route("/all")
@login_required
async def get_all_posts():
    username = current_user.id
    user = requests.request("GET", url=f"{url}/user/{username}", headers={'accept': 'application/json'})
    response = requests.request("GET", url=f"{url}/post/{current_user.id}", headers={'accept': 'application/json'})
    blog_posts = response.json().get("posts")
    blog_posts_date = []
    for post in blog_posts:
        date = datetime.datetime.fromisoformat(post["date"]).strftime("%b %d %Y %I:%M%p")
        post["date"] = date
        blog_posts_date.append(post)

    return await render_template("posts.html", user=user.json(), blog_posts=blog_posts_date)
