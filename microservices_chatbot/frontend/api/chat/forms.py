import quart.flask_patch
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    text = StringField('Enter text', validators=[DataRequired()])
    send = SubmitField("Send")
