from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView

from puppy import db
from puppy.api.models import Puppy, Owner
from puppy.api.schemas import (
    PuppySchema, PuppiesSchema, GetPuppySchema,
    AddOwnerSchema, GetOwnerSchema, OwnerPuppy
)


blueprint = Blueprint("puppy", __name__, description="Puppy Api",)


@blueprint.route("/all")
class GetAll(MethodView):

    @blueprint.response(PuppiesSchema, description="List of all puppies.")
    def get(self):
        """Get all puppies"""
        puppies = Puppy.query.all()
        return {"puppies": puppies}


@blueprint.route("/add")
class AddPuppy(MethodView):

    @blueprint.arguments(PuppySchema, description="Add puppy.")
    @blueprint.response(PuppiesSchema, description="Puppy added.")
    def post(self, data: PuppySchema):
        """Add pupy name."""
        puppy = Puppy(name=data["name"])
        db.session.add(puppy)
        db.session.commit()
        puppies = Puppy.query.all()
        return {'puppies': puppies}


@blueprint.route("/puppy/<int:id>")
class PuppyId(MethodView):

    @blueprint.response(OwnerPuppy)
    def get(self, id: int):
        """Get puppy by id."""
        try:
            puppy = Puppy.query.get(id)
            # owner = Owner.query.filter_by(puppy_id=id).all()
            print(puppy)
        except:
            return {"error": "Unknown error."}
        return puppy

    @blueprint.arguments(PuppySchema, location="json")
    @blueprint.response(GetPuppySchema)
    def put(self, data, id: int):
        """Update puppy by id."""
        pup = Puppy.query.get(id)
        pup.name = data.get("name")
        db.session.commit()
        return pup

    @blueprint.response()
    def delete(self, id: int):
        """Delete puppy by id."""
        try:
            pup = Puppy.query.get(id)
            db.session.delete(pup)
            db.session.commit()
        except:
            pass
        return {}


@blueprint.route("/owner/")
class AddOwner(MethodView):

    @blueprint.arguments(AddOwnerSchema, location="json")
    @blueprint.response(GetOwnerSchema)
    def post(self, data):
        """Add Owner for puppy."""
        owner = Owner(name=data.get("name"),
                      puppy_id=data.get("puppy_id"))
        db.session.add(owner)
        db.session.commit()
        return owner


@blueprint.errorhandler(500)
def error500(error):
    return {"error": 500}
