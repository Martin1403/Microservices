from flask import abort, render_template, request
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

from users.api.dal import user_dal
from users.api.schemas import (
    UserIdSchema, GetUserSchema, CheckUserSchema,
    UpdateUserSchema, AllUsersSchema,)


blueprint = Blueprint('users', __name__, description='Users API')


@blueprint.route("/")
def index():
    """Home page.
    """
    return render_template("index.html")


@blueprint.route("/user")
class User(MethodView):
    """ Register User and Get all users """

    @blueprint.response(AllUsersSchema)
    def get(self):
        """Get all users."""
        with user_dal() as ud:
            users = ud.get_all_users()
        return users, 200

    @blueprint.arguments(UpdateUserSchema, location="json")
    @blueprint.response(GetUserSchema)
    def post(self, data):
        """Create user."""
        with user_dal() as ud:
            user = ud.register_user(data)
            if user:
                return user, 200
        abort(500, description="Email or username exists.")


@blueprint.route("/user/<int:user_id>")
class UserId(MethodView):
    """ User ID """

    @blueprint.response(GetUserSchema)
    def get(self, user_id):
        """Get user by id."""
        with user_dal() as ud:
            user = ud.get_user_id(user_id)
            if user:
                return user, 200
        abort(404, description=f'User with ID {user_id} not found')

    @blueprint.arguments(UpdateUserSchema, location="json")
    @blueprint.response(GetUserSchema)
    def put(self, data, user_id):
        """Update user by id."""
        with user_dal() as ud:
            user = ud.update_user_id(user_id=user_id, data=data)
            if user:
                return user
        abort(404, description=f'User with ID {user_id} not found')

    @blueprint.response(GetUserSchema)
    def delete(self, user_id):
        """Delete user by id."""
        with user_dal() as ud:
            user = ud.delete_user_id(user_id)
            if user:
                return user, 204
        abort(404, description=f'User with ID {user_id} not found')


@blueprint.route("/check", methods=["POST"])
@blueprint.arguments(CheckUserSchema, location="json")
@blueprint.response(GetUserSchema)
def check_password_email(data):
    """Check password."""
    with user_dal() as ud:
        user = ud.check_password_email(data)
        if user:
            return user, 200
        elif user == False:
            abort(422, description=f'Wrong password.')
        elif user == None:
            abort(404, description=f'No user with {data["email"]}')
        else:
            raise NotImplemented("Something wrong happens.")


@blueprint.app_errorhandler(500)
def error_500(e):
    return {"code": 500, "status": str(e)}, 500


@blueprint.app_errorhandler(404)
def error_404(e):
    return {"code": 404, "status": str(e)}, 404


@blueprint.app_errorhandler(422)
def error_422(e):
    return {"code": 422, "status": str(e)}, 422
