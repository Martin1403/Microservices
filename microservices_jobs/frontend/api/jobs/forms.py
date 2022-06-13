from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField


class CreateJobForm(FlaskForm):
    title = StringField("Title: ")
    description = TextAreaField("Description: ")
    submit = SubmitField("Submit")


class CreateCompanyForm(FlaskForm):
    name = StringField("Name: ")
    description = TextAreaField("Description: ")
    submit = SubmitField("Submit")
