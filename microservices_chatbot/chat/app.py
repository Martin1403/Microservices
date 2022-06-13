import os
from quart import Quart, render_template

# APP SETUP
app = Quart(__name__)
app.config["BASE_FOLDER_PATH"] = os.path.abspath(os.path.join(os.path.dirname(__name__), "chat"))
app.config["DATABASE_FOLDER_PATH"] = os.path.join(app.config["BASE_FOLDER_PATH"], "database")
app.config["DATABASE_URI_PATH"] = os.path.join(app.config["DATABASE_FOLDER_PATH"], "test.db")
os.makedirs(app.config["DATABASE_FOLDER_PATH"], exist_ok=True)

# CLICK COMMANDS
from chat.api.tests.asyncrun import test_async
from chat.api.tests.initialize import init_db
from chat.api.tests.database import test_db
from chat.api.tests.dal import test_dal
app.cli.add_command(test_async)
app.cli.add_command(init_db)
app.cli.add_command(test_db)
app.cli.add_command(test_dal)


# REGISTER BLUEPRINTS
from chat.api.graphql import blueprint
app.register_blueprint(blueprint)
