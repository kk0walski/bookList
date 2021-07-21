from flask import Blueprint, jsonify, request
from .model import Book

api = Blueprint('api', __name__,  url_prefix="/api")


@api.route('/books')
def show_books():
    reasult = {}
    books = Book.query

    query_data = {
        'title': request.args.get('title'),
        'author': request.args.get('author'),
        'language': request.args.get('language'),
        'date_from': request.args.get('date_from'),
        'date_to': request.args.get('date_to')
    }

    if query_data['title']:
        books = books.filter(Book.title.like(
            "%{}%".format(query_data['title'])))
    if query_data['author']:
        books = books.filter(Book.author.like(
            "%{}%".format(query_data['author'])))
    if query_data['language']:
        books = books.filter(Book.language == query_data['language'])
    if query_data['date_from']:
        books = books.filter(Book.date >= query_data['date_from'])
    if query_data['date_to']:
        books = books.filter(Book.date <= query_data['date_to'])

    for book in books:
        reasult[book.isbn] = book.serialize
    return jsonify(reasult), 200
