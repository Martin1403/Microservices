import quart.flask_patch
from quart import Quart, render_template
from flask_login import LoginManager

# APP CONFIG
app = Quart(__name__)
app.config["WTF_CSRF_SECRET_KEY"] = "A SECRET KEY"
app.config["SECRET_KEY"] = "ANOTHER ONE"

# FLASK LOGIN MANAGER
from frontend.api.base.views import User
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(id):
    user = User()
    user.id = id
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return render_template("401.html")


# REGISTER BLUEPRINTS
from frontend.api.base.views import core
from frontend.api.chat.views import chats
from frontend.api.measure.views import measurements
app.register_blueprint(core)
app.register_blueprint(chats)
app.register_blueprint(measurements)

