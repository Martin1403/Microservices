import os

import quart.flask_patch
from flask_login import LoginManager, UserMixin
from quart import Quart, render_template

try:
    from core.views import core
    from users.views import users, User
    from errors.handlers import error
    from posts.views import posts

except ImportError:
    from frontend.core.views import core
    from frontend.users.views import users, User
    from frontend.errors.handlers import error
    from frontend.posts.views import posts


app = Quart(__name__)
# REGISTER BLUEPRINTS
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error)
app.register_blueprint(posts)

# SETUP SECRET KEYS
app.config["WTF_CSRF_SECRET_KEY"] = "A SECRET KEY"
app.config["SECRET_KEY"] = "ANOTHER ONE"
# SETUP LOGIN MANAGER
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


if __name__ == "__main__":
    app.run(
        port=os.environ.get("PORT") or 5000,
        host=os.environ.get("HOST") or "127.0.0.1",
        debug=os.environ.get("DEBUG") or True,
        )
