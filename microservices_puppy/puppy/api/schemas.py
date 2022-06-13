from marshmallow import Schema, fields, validate, EXCLUDE


class IdPuppySchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True)


class PuppySchema(Schema):

    name = fields.String(required=True)


class OwnerPuppy(PuppySchema):

    owner = fields.String(required=False)


class GetPuppySchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True)
    name = fields.String(required=True)


class PuppiesSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    puppies = fields.List(fields.Nested(GetPuppySchema), required=True)


class AddOwnerSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(required=True)
    puppy_id = fields.Integer(required=True)


class GetOwnerSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    puppy_id = fields.Integer(required=True)
