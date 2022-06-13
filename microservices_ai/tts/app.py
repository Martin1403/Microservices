import os
from quart import Quart
from quart_schema import QuartSchema


# APP SETTINGS
app = Quart(__name__)
QuartSchema(app, title="PytorchTTS APP", version="0.0.1")

# REGISTER BLUEPRINTS
from tts.api.views import blueprint
app.register_blueprint(blueprint)

# COMMANDS
from tts.api.commands import test_async
app.cli.add_command(test_async)

