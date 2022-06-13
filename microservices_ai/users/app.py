import os
import os
from quart import Quart

# APP SETUP
app = Quart(__name__)
app.config["BASE_FOLDER_PATH"] = os.path.abspath(os.path.join(os.path.dirname(__name__), "users"))
app.config["DATABASE_FOLDER_PATH"] = os.path.join(app.config["BASE_FOLDER_PATH"], "database")
app.config["DATABASE_URI_PATH"] = os.path.join(app.config["DATABASE_FOLDER_PATH"], "test.db")
os.makedirs(app.config["DATABASE_FOLDER_PATH"], exist_ok=True)

# REGISTER BLUEPRINTS
from users.api.graphql import blueprint
app.register_blueprint(blueprint)

# CLICK COMMANDS
from users.api.commands import test_async, init_db, test_dal
app.cli.add_command(test_async)
app.cli.add_command(init_db)
app.cli.add_command(test_dal)
