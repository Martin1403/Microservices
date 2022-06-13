import os
import requests
import datetime
from dataclasses import asdict
from typing import Tuple, Type, Union, Optional, List
from pydantic.dataclasses import dataclass
from quart import (
    Blueprint, render_template, redirect, request
)
from quart_schema import (
    validate_response, validate_request)

from .dal import blog_post_dal, user_dal


posts = Blueprint("posts", __name__)

url = "http://emotions-service-c:5002/" if os.environ.get("DOCKER") else "http://127.0.0.1:5002"
# url = "http://posts-service-c:5001/" if os.environ.get("DOCKER") else "http://127.0.0.1:5001"

@dataclass
class ErrorSchema:
    """Error handler."""
    error: str


@dataclass
class PostSchema:
    """Created post."""
    id: int
    user_id: int
    date: datetime.datetime
    title: str
    text: str
    emotion: str


@dataclass
class PostsSchema:
    """List of created posts."""
    posts: List[PostSchema]


@posts.route("/post/<username>")
@validate_response(PostsSchema, status_code=200)
@validate_response(ErrorSchema, status_code=500)
async def get_posts_by_username(username: str) -> Tuple[Union[PostsSchema, ErrorSchema], int]:
    """Get all posts by username.
    The function returns all user posts.
    """
    try:
        async with blog_post_dal() as bp:
            blog_posts = await bp.get_all_posts_by_username(username)
        return blog_posts, 200

    except ValueError as error:
        error = ErrorSchema(error=str(error))
        return error, 500


@dataclass
class BaseSchema:
    title: str
    text: str


@dataclass
class CreatePostSchema(BaseSchema):
    """Attributes to create post."""
    username: str


@posts.route("/post/create", methods=["POST"])
@validate_request(CreatePostSchema)
@validate_response(PostSchema, status_code=200)
@validate_response(ErrorSchema, status_code=500)
async def create_post(data: PostSchema) -> Tuple[Union[PostSchema, ErrorSchema], int]:
    """Create post.
    The function creates a post for user by username.
    """
    def get_emotion(text):
        """Get emotion from text."""
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        response = requests.request("POST", url=f"{url}/emotions", json={"text": text}, headers=headers)
        return response.json().get("emotion") or "joy"

    try:
        async with blog_post_dal() as bd:
            post = await bd.create_blog_post_username(
                username=data.username, title=data.title, text=data.text, emotion=get_emotion(data.text))
        return post, 200
    except ValueError as error:
        error = ErrorSchema(error=str(error))
        return error, 500


@dataclass
class IdPostSchema:
    id: int


@dataclass
class UpdatePostSchema(IdPostSchema, BaseSchema):
    """Update schema"""
    pass


@posts.route("/post/update", methods=["PUT"])
@validate_request(UpdatePostSchema)
@validate_response(PostSchema, status_code=200)
@validate_response(ErrorSchema, status_code=500)
async def update_post(data: UpdatePostSchema):
    """Update post.
    The function update a post for user by id.
    """
    try:
        async with blog_post_dal() as bd:
            post = await bd.update_blog_post_id(
                id=data.id, title=data.title, text=data.text)
        return post, 200
    except ValueError as error:
        error = ErrorSchema(error=str(error))
        return error, 500


@dataclass
class NoContentSchema:
    """No content schema"""
    pass


@posts.route("/post/delete", methods=["DELETE"])
@validate_request(IdPostSchema)
@validate_response(NoContentSchema, status_code=204)
@validate_response(ErrorSchema, status_code=500)
async def delete_post(data: IdPostSchema):
    """Delete post.
    The function delete a post by id.
    """
    try:
        async with blog_post_dal() as bd:
            await bd.delete_blog_post_id(id=data.id)
        return NoContentSchema(), 204
    except ValueError as error:
        error = ErrorSchema(error=str(error))
        return error, 500
