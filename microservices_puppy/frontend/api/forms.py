from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class ShowForm(FlaskForm):
    pass


class UpdateForm(FlaskForm):
    name = StringField("Name of Puppy: ")
    submit = SubmitField("Update Puppy")


class AddForm(FlaskForm):
    name = StringField("Name of Puppy: ")
    submit = SubmitField("Add Puppy")


class DelForm(FlaskForm):
    id = IntegerField("Id Number of Puppy to Remove: ")
    submit = SubmitField("Remove Puppy")


class GetForm(FlaskForm):
    id = IntegerField("Insert puppy id: ")
    submit = SubmitField("Get Puppy")


class AddOwnerForm(FlaskForm):
    id = IntegerField("Insert puppy id: ")
    name = StringField("Owner's name: ")
    submit = SubmitField("Add owner")
