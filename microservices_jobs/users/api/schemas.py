from marshmallow import Schema, fields, EXCLUDE


class UserIdSchema(Schema):
    """User Id"""
    class Meta:
        unknown = EXCLUDE
    user_id = fields.String(required=True)


class LoginSchema(Schema):
    """User credentials"""

    class Meta:
        unknown = EXCLUDE
    username = fields.String(required=True)
    email = fields.String(required=True)


class GetUserSchema(UserIdSchema, LoginSchema):
    """User credentials"""
    class Meta:
        unknown = EXCLUDE
    password = fields.String(required=True)


class UpdateUserSchema(LoginSchema):
    """User credentials"""

    class Meta:
        unknown = EXCLUDE
    password = fields.String(required=True)


class CheckUserSchema(Schema):
    """ Check password by email."""
    class Meta:
        unknown = EXCLUDE
    email = fields.String(required=True)
    password = fields.String(required=True)


class AllUsersSchema(Schema):
    users = fields.List(fields.Nested(GetUserSchema), required=False)
