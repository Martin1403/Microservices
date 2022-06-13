import click

from chat.api.models import engine, Base
from chat.api.tests.asyncrun import async_run


@click.command("init-db")
@async_run
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    click.echo("Initialize ok...")
