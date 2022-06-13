import os
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))

from frontend.api.views import blueprint

app.register_blueprint(blueprint)
