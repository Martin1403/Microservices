from dataclasses import asdict
from typing import Tuple, Type, Union, Optional
from pydantic.dataclasses import dataclass
from quart import (
    Blueprint, render_template, redirect, request
)
from quart_schema import (
    validate_response, validate_request)

from .dal import user_dal

users = Blueprint("users", __name__)


@users.route("/")
async def index():
    """Home page.
    The function render index.html
    """
    return await render_template("index.html")


@dataclass
class ErrorSchema:
    """Error handler."""
    error: str


@dataclass
class GetUserSchema:
    """Get User Schema."""
    email: str
    password: str


@dataclass
class CreateUserSchema(GetUserSchema):
    """Create User Schema."""
    username: str


@dataclass
class UserSchema(CreateUserSchema):
    """User schema."""
    id: int
    profile_image: str


@dataclass
class UpdateUserSchema:
    username: str
    new_username: Optional[str]
    new_email: Optional[str]
    new_picture: Optional[str]


@users.route("/create", methods=["POST"])
@validate_request(CreateUserSchema)
@validate_response(UserSchema, status_code=200)
@validate_response(ErrorSchema, status_code=500)
async def create_user(data: CreateUserSchema) -> Tuple[Union[UserSchema, ErrorSchema], int]:
    """Create user.
    The function creates a new user.
    """
    try:
        async with user_dal() as bd:
            user = await bd.create_user(
                username=data.username,
                email=data.email,
                password=data.password
            )

        return user, 200
    except ValueError as error:
        error = ErrorSchema(error=str(error))
        return error, 500


@users.route("/user", methods=["POST"])
@validate_request(GetUserSchema)
@validate_response(UserSchema, status_code=200)
@validate_response(ErrorSchema, status_code=500)
async def get_user_email_password(data: GetUserSchema) -> Tuple[Union[CreateUserSchema, ErrorSchema], int]:
    """Get user by email.
    The function returns user by email. Also validates if email and password are correct.
    """
    try:
        async with user_dal() as bd:
            user = await bd.get_user_by_email(
                email=data.email,
                password=data.password
            )
        return user, 200
    except ValueError as error:
        error = ErrorSchema(error=str(error))
        return error, 500


@users.route("/user/<username>", methods=["GET"])
@validate_response(UserSchema, status_code=200)
@validate_response(ErrorSchema, status_code=500)
async def get_user_name(username: str) -> Tuple[Union[UserSchema, ErrorSchema], int]:
    """Get user by name.
    The function returns user by name.
    """
    try:
        async with user_dal() as bd:
            user = await bd.get_user_by_username(
                username=username
            )
        return user, 200
    except ValueError as error:
        error = ErrorSchema(error=str(error))
        return error, 500


@users.route("/update", methods=["PUT"])
@validate_request(UpdateUserSchema)
@validate_response(UserSchema, status_code=200)
@validate_response(ErrorSchema, status_code=500)
async def update_user(data: UpdateUserSchema):
    """Update user.
    The function updates user credentials.
    """
    try:
        async with user_dal() as bd:
            user = await bd.update_user_by_username(
                data=data
            )
        return user, 200
    except ValueError as error:
        error = ErrorSchema(error=str(error))
        return error, 500
