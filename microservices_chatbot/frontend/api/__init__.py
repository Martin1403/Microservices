from __future__ import annotations
import os
from typing import Optional

import requests

# Url for all endpoints:
url_for_chat = "http://chat-service-c:5001/graphql" \
    if os.environ.get("DOCKER") else "http://127.0.0.1:5001/graphql"

url_for_ai = "http://ai-service-c:5002" \
    if os.environ.get("DOCKER") else "http://127.0.0.1:5002"

# Headers:
headers = {'accept': 'application/json'}
content_headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

logs: Optional[dict] = None


def post_request(query, id=None, input=None):
    return requests.request(
        method="POST",
        url=url_for_chat,
        json={'query': query, "variables": {"id": id, "input": input}},
        headers=content_headers
    )


def get_logs(reset=False):
    global logs
    if not logs or reset:
        logs = {"count": 0, "logs": []}
    return logs


class UserCache(dict):
    def __init__(self, user):
        super().__init__()
        self.update(user)


cache: Optional[UserCache] = None


def save_user(user_object) -> None:
    global cache
    cache = UserCache(user_object)


def get_user() -> UserCache:
    global cache
    return cache
