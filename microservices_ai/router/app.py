from quart import Quart
from quart_schema import QuartSchema


# APP SETTINGS
app = Quart(__name__)
QuartSchema(app, title="Router API", version="0.0.1")

# REGISTER BLUEPRINTS
from router.api.views import blueprint
from router.api.router.routes import router
app.register_blueprint(blueprint)
app.register_blueprint(router)

# COMMANDS
from router.api.commands import test_async
app.cli.add_command(test_async)

