import os
from quart import Quart
from quart_schema import QuartSchema

# APP SETTINGS
app = Quart(__name__)
QuartSchema(app, title="Chat Api", version="0.0.1")

# REGISTER BLUEPRINTS
from ai.api.routes import blueprint
app.register_blueprint(blueprint)

# CLICK COMMANDS
from ai.api.asyncrun import test_async
from ai.api.achat import test_async_chat
app.cli.add_command(test_async)
app.cli.add_command(test_async_chat)
