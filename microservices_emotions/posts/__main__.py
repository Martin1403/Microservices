import os

from quart import Quart
from quart_schema import QuartSchema

try:
    from api.user_routes import users
    from api.post_routes import posts
    from api.models import Base, engine, database_path
    from api.dal import user_dal, blog_post_dal

except ImportError:
    from posts.api.user_routes import users
    from posts.api.post_routes import posts
    from posts.api.models import Base, engine, database_path
    from posts.api.dal import user_dal, blog_post_dal


app = Quart(__name__)
app.register_blueprint(users)
app.register_blueprint(posts)
QuartSchema(app, title="Posts Api", version="0.0.1")


@app.before_serving
async def startup():
    """Create db tables."""
    if not os.path.exists(database_path) or True:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    app.run(
        port=os.environ.get("PORT") or 5001,
        host=os.environ.get("HOST") or "127.0.0.1",
        debug=os.environ.get("DEBUG") or True,
        )
