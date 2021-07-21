import re
from flask import current_app
from datetime import datetime
from flask import Blueprint, render_template, redirect
from flask.helpers import url_for
from .forms import SearchForm, ImportForm
from urllib.parse import urlencode
from .model import Book, db
import requests

import_books = Blueprint("import", __name__,  url_prefix="/import")


def get_isbn(book):
    identifiers = book.get('volumeInfo', {}).get('industryIdentifiers', [])
    if identifiers:
        identifiers_dict = {}
        for identifier_dict in identifiers:
            identifiers_dict[identifier_dict['type']
                             ] = identifier_dict['identifier']
        if identifiers_dict.get('ISBN_10'):
            return identifiers_dict.get('ISBN_10')
        else:
            return identifiers[0].get('identifier')
    else:
        return None


def map_book(book):
    isbn = get_isbn(book)
    return isbn, {
        'title': book.get('volumeInfo', {}).get('title', 'no_title'),
        'author': ', '.join(book.get('volumeInfo', {}).get('authors', ['annonymous'])),
        'date': book.get('volumeInfo', {}).get('publishedDate', None),
        'pages': book.get('volumeInfo', {}).get('pageCount', None),
        'language': book.get('volumeInfo', {}).get('language', 'no-lang'),
        'url': book.get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail', None)
    }


def get_books_dict(items):
    reasult = {}
    for book in items:
        key, book = map_book(book)
        if key:
            reasult[key] = book
    return reasult


def list_to_dict(list):
    if list:
        return [(lambda d: d.update(isbn=key) or d)(val)
                for (key, val) in list.items()]
    else:
        return None


def None_at_top(books):
    if books:
        return list(filter(lambda x: x['url'] != None, books)) + list(
            filter(lambda x: x['url'] == None, books))
    else:
        return None


def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data['items']
        reasult = get_books_dict(items)
        reasult_list = list_to_dict(reasult)
        reasult_books = None_at_top(reasult_list)
        return reasult_books


def build_querystring(query):
    query_data = dict(
        filter(lambda elem: elem[1] != '' or elem[0] == 'q', query.items()))
    querystring = urlencode(query_data)
    querystring = querystring.replace('&', '+')
    querystring = querystring.replace('=', ':')
    querystring = querystring.replace(':', '=', 1)
    if query_data['q'] == '':
        querystring = querystring.replace('+', '', 1)
    return querystring


@import_books.route('/', methods=['GET', 'POST'])
def books():
    search = SearchForm()
    if search.validate_on_submit():
        query_data = {
            'q': search.search.data,
            'intitle': search.title.data,
            'inauthor': search.author.data,
            'inpublisher': search.publisher.data,
            'subject': search.subject.data,
            'isbn': search.subject.data,
        }
        querystring = build_querystring(query_data)
        return redirect(url_for('import.append_books', query=querystring))
    return render_template('import.html', form=search)


def database_commit(import_form):
    if import_form.validate():
        books = import_form.books.entries
        for book in books:
            new_book = Book(isbn=book.isbn.data, author=book.author.data, title=book.title.data,
                            date=book.date.data, pages=book.pages.data, url=book.url.data,
                            language=book.language.data)
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('books.show_books'))
    else:
        return render_template('import2.html', form=import_form)


def get_date(book_date):
    if book_date and re.match(r"\d{4}-\d{2}-\d{2}", book_date):
        return datetime.strptime(book_date, '%Y-%m-%d').date()
    else:
        return None


def render_books_form(import_form, books):
    if books:
        for book in books:
            book['date'] = get_date(book['date'])
            import_form.books.append_entry(book)
        return render_template('import2.html', form=import_form)
    else:
        return redirect(url_for('books.show_books'))


@import_books.route('/append/<query>', methods=['GET', 'POST'])
def append_books(query):
    import_form = ImportForm()
    if import_form.remove.data:
        import_form.books.pop_entry()
        return render_template('import2.html', form=import_form)
    elif import_form.submit.data:
        return database_commit(import_form)
    else:
        url = 'https://www.googleapis.com/books/v1/volumes?' + query
        books = get_request(url)
        return render_books_form(import_form, books)
