import os
import requests


def make_post_request(end: str, data: dict) -> requests.request:
    """
    Post request to router
    :param end: Endpoint
    :param data: Data to send
    :return: post request
    """
    return requests.request(
        "POST", json=data, headers={"accept": "application/json", "Content-Type": "application/json"},
        url=f"http://router-service-c:5001/{end}" if os.environ.get("DOCKER") else f"http://127.0.0.1:5001/{end}")
