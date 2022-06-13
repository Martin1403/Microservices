import click
import asyncio
from functools import wraps

from typing import List, Optional

async def test_function():
    return "Some"

class Test(object):

    async def __aenter__(self):
        await test_function()
        print("enter")

    async def __aexit__(self, *args):
        print("exit")

    def __await__(self):
        return self.__aenter__().__await__()


def async_run(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


@click.command("test-async")
@async_run
async def test_async():
    async with Test():
        print("Hello")
    await Test()
    click.echo("Async ok...")
