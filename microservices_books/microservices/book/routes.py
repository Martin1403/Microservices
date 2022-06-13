from flask import Blueprint, jsonify, \
    request, make_response

from models import Book
from models import db

book_blueprint = Blueprint("book_api_routes",
                           __name__,
                           url_prefix="/api/book")


@book_blueprint.route("/all", methods=["GET"])
def get_all_books():
    all_books = Book.query.all()
    all_books = [book.serialize() for book in all_books]
    response = {"result": all_books}
    return jsonify(response)


@book_blueprint.route("/create", methods=["POST"])
def create_book():
    try:
        book = Book()
        book.name = request.form["name"]
        book.slug = request.form["slug"]
        book.image = request.form["image"]
        book.price = request.form["price"]

        db.session.add(book)
        db.session.commit()
        response = {"message": "Book created", "result": book.serialize()}
    except Exception as e:
        response = {"message": "Book creation failed"}

    return jsonify(response)


@book_blueprint.route("/<slug>", methods=["GET"])
def book_details(slug):
    book = Book.query.filter_by(slug=slug).first()
    if book:
        response = {"result": book.serialize()}
    else:
        response = {"message": "No book found"}
    return make_response(jsonify(response), 200)

