import quart.flask_patch
from quart import Quart

# APP SETTINGS
app = Quart(__name__)
app.config["WTF_CSRF_SECRET_KEY"] = "A SECRET KEY"
app.config["SECRET_KEY"] = "ANOTHER ONE"

# REGISTER BLUEPRINTS
from frontend.api.views import blueprint
from frontend.api.users.views import users
app.register_blueprint(blueprint)
app.register_blueprint(users)
