from flask import Flask, render_template
from flask_login import LoginManager

from frontend.api.users.views import User
from frontend.config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return render_template("401.html")

from frontend.api.core.views import core
from frontend.api.users.views import users
from frontend.api.jobs.views import jobs

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(jobs)

