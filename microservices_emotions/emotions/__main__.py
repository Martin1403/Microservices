import os
import warnings
from typing import Tuple, Union

from quart import Quart, render_template
from pydantic.dataclasses import dataclass
from quart_schema import QuartSchema, validate_request, validate_response

try:
    from api.errors import error
    from api.routes import blueprint
except ImportError as err:
    from emotions.api.errors import error
    from emotions.api.routes import blueprint
    print(err)



app = Quart(__name__)
app.register_blueprint(error)
app.register_blueprint(blueprint)
QuartSchema(app, title="Emotions Api", version="0.0.1")


if __name__ == '__main__':
    app.run(
        host=os.environ.get("HOST") or "127.0.0.1",
        port=os.environ.get("PORT") or 5002,
        debug=os.environ.get("DEBUG") or True,
    )

