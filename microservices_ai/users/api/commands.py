import click

from users.api.actions import async_run
from users.api.models import engine, Base
from users.api.tests.asyncrun import AsyncTest
from users.api.dal import user_dal


@click.command("test-async")
@async_run
async def test_async():
    async with AsyncTest() as test:
        async_object = await test
    click.echo(async_object.text)


@click.command("init-db")
@async_run
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    click.echo("Initialize ok...")


@click.command("test-dal")
@async_run
async def test_dal():
    data = {"username": "John",
            "email": "example@example.xxx",
            "password": "12345"}
    async with user_dal() as ud:
        user = await ud.create_user(data)
    click.echo(user)

    click.echo(f"Data access layer ok...")
