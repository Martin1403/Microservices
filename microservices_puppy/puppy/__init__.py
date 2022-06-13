import os.path

from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask import Flask, redirect, render_template
from flask.views import MethodView

from puppy.config import BaseConfig, database

app = Flask(__name__)
app.config.from_object(BaseConfig)

puppy_api = Api(app)
db = SQLAlchemy(app)
Migrate(app, db, directory=os.path.join(database, "migrations"))


@app.route("/")
def home():
    return render_template("index.html")


from puppy.api.views import blueprint
puppy_api.register_blueprint(blueprint)
