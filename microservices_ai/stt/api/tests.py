import asyncio
from functools import wraps


class AsyncTest(object):
    """Async Class"""
    def __init__(self):
        self.text = "HelloWorld!!!"

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    def __await__(self):
        return self.__aenter__().__await__()


def async_run(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper
