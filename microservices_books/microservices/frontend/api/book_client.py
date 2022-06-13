import requests
from . import BOOK_API_URL


class BookClient:
    @staticmethod
    def get_books():
        response = requests.get(BOOK_API_URL + "/api/book/all")
        return response.json()

    @staticmethod
    def get_book(slag):
        response = requests.get(BOOK_API_URL + "/api/book/" + slag)
        return response.json()