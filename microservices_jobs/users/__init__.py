from flask import Flask
from flask_smorest import Api


from users.config import BaseConfig
from users.api.models import Base, engine

app = Flask(__name__)

app.config.from_object(BaseConfig)

users_api = Api(app)

Base.metadata.create_all(bind=engine)
from users.api.routes import blueprint
users_api.register_blueprint(blueprint)