import asyncio
from functools import wraps


def action_endpoint(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        result = await f(*args, **kwargs)
        print(result)
        return {"text": "HelloWorld"}
    return decorated_function


def async_run(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper
