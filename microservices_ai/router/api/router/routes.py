from typing import Optional, Any, Dict, Tuple, Union, NewType, Mapping

from quart import Blueprint
from quart_schema import validate_request, validate_response
from pydantic.dataclasses import dataclass

from router.api.router.actions import router_action, register_action


router = Blueprint("router", __name__)

@dataclass
class DataSchema:
    """Data from frontend"""
    data: str


@router.route("/router", methods=["POST"])
@validate_request(DataSchema)
@validate_response(DataSchema)
@router_action
async def xxx(data: DataSchema):
    return data


@dataclass
class IdSchema:
    """User id"""
    id: str


@dataclass
class UserSchema:
    """Register User"""
    username: str
    email: str
    password: str


@dataclass
class ErrorSchema:
    """Error"""
    error: str


@router.route("/register", methods=["POST"])
@validate_request(UserSchema)
@validate_response(IdSchema, status_code=200)
@validate_response(ErrorSchema, status_code=409)
@register_action
async def register(data: DataSchema):
    return data

