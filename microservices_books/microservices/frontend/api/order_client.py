import requests
from . import ORDER_API_URL
from flask import session


class OrderClient:
    @staticmethod
    def get_order():
        headers = {"Authorization": session["user_api_key"]}
        response = requests.get(ORDER_API_URL + "/api/order", headers=headers)
        return response.json()

    @staticmethod
    def add_to_cart(book_id, quantity=1):
        payload = {
            "book_id": book_id,
            "quantity": quantity,
        }
        headers = {"Authorization": session["user_api_key"]}
        response = requests.post(f"{ORDER_API_URL}/api/order/add-item",
                                 data=payload, headers=headers)

        return response.json()

    @staticmethod
    def checkout():
        headers = {"Authorization": session["user_api_key"]}
        response = requests.post(f"{ORDER_API_URL}/api/order/checkout", headers=headers)
        return response.json()

    @staticmethod
    def get_order_from_session():
        default_order = {
            "items": {}
        }
        return session.get("order", default_order)
    