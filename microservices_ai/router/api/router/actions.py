import os
import requests
from dataclasses import asdict
from functools import wraps
from quart import redirect, url_for

url_users = f"http://users-service-c:5002/graphql" if os.environ.get("DOCKER") else f"http://127.0.0.1:5002/graphql"
create_user_query = """
mutation CreateUser($input: CreateUserInput) {
  user: CreateUser(input: $input) {
    id
  }
}
"""


def post_request(query, url, id=None, input=None):
    return requests.request(method="POST", url=url,
        json={'query': query, "variables": {"id": id, "input": input}},
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )


def router_action(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        data = await f(*args, **kwargs)
        return {"data": data.data}
    return decorated_function


def register_action(f):
    """Register user"""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        data = await f(*args, **kwargs)
        response = post_request(query=create_user_query, url=url_users, input=asdict(data))
        response = response.json().get("data").get("user")
        return response if response else {"error": "Username or email already exists."}, 409
    return decorated_function
