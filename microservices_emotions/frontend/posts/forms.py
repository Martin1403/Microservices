from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField("Post")


class UpdateBlogPostForm(FlaskForm):
    id = IntegerField()
    title = StringField("Title", validators=[], render_kw={"placeholder": "Title"})
    text = TextAreaField("Text", validators=[], render_kw={"placeholder": "Text"})
    update = SubmitField("Update")
    delete = SubmitField("Delete")
