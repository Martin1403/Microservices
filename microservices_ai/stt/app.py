import os
from quart import Quart
from quart_schema import QuartSchema

# APP SETTINGS
app = Quart(__name__)
QuartSchema(app, title="DeepSpeech API", version="0.0.1")

# REGISTER BLUEPRINTS
from stt.api.views import blueprint
app.register_blueprint(blueprint)

# COMMANDS
from stt.api.commands import test_async, test_model
app.cli.add_command(test_async)
app.cli.add_command(test_model)
