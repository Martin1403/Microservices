import os
from flask import g
from flask import Flask
from flask_login import LoginManager, user_loaded_from_request
from routes import user_blueprint
import models
from flask_migrate import Migrate
from flask.sessions import SecureCookieSessionInterface

os.makedirs("database", exist_ok=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = 'yol_voq7'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./database/user.db"
models.init_app(app)
app.register_blueprint(user_blueprint)
login_manager = LoginManager(app)
migrate = Migrate(app, models.db)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001)

