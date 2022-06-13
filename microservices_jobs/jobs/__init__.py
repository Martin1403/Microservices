import os
from flask import Flask
from flask_migrate import Migrate


# APP CONFIG
from jobs.config import BaseConfig, BASE
app = Flask(__name__)
app.config.from_object(BaseConfig)

# CLI COMMANDS
from jobs.api.tests import init_db, test_db, dal_adapter
app.cli.add_command(init_db)
app.cli.add_command(test_db)
app.cli.add_command(dal_adapter)

# MIGRATE DATABASE
from jobs.api.models import db
Migrate(app, db, directory=os.path.join(BASE, "migrations"))


# BLUEPRINTS
from jobs.api.blueprint import blueprint
app.register_blueprint(blueprint)
