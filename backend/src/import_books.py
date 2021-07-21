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
    if isbn:
        return isbn, {
            'title': book.get('volumeInfo', {}).get('title', 'no_title'),
            'author': ', '.join(book.get('volumeInfo', {}).get('authors', ['annonymous'])),
            'date': book.get('volumeInfo', {}).get('publishedDate', None),
            'pages': book.get('volumeInfo', {}).get('pageCount', None),
            'language': book.get('volumeInfo', {}).get('language', 'no-lang'),
            'url': book.get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail', None)
        }


def get_request(url):
    response = requests.get(url)
    reasult = {}
    if response.status_code == 200:
        data = response.json()
        items = data['items']
        for book in items:
            key, book = map_book(book)
            if key:
                reasult[key] = book
        reasult_list = [(lambda d: d.update(isbn=key) or d)(val)
                        for (key, val) in reasult.items()]
        reasult_books = list(filter(lambda x: x['url'] != None, reasult_list)) + list(
            filter(lambda x: x['url'] == None, reasult_list))
        return reasult_books


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
        query_data = dict(
            filter(lambda elem: elem[1] != '' or elem[0] == 'q', query_data.items()))
        querystring = urlencode(query_data)
        querystring = querystring.replace('&', '+')
        querystring = querystring.replace('=', ':')
        querystring = querystring.replace(':', '=', 1)
        if query_data['q'] == '':
            querystring = querystring.replace('+', '', 1)
        return redirect(url_for('import.append_books', query=querystring))
    return render_template('import.html', form=search)


def fix_date(date):
    elements = date.split('-')
    if len(elements) == 1:
        if elements[0][-1] == "*":
            elements[0] = elements[0][:-1]
        elements.append('01')
        elements.append('01')
        return '-'.join(elements)
    elif len(elements) == 2:
        elements.append('01')
        return '-'.join(elements)
    elif len(elements) == 3:
        return '-'.join(elements)
    else:
        return '0001-01-01'


@import_books.route('/append/<query>', methods=['GET', 'POST'])
def append_books(query):
    import_form = ImportForm()
    if import_form.remove.data:
        import_form.books.pop_entry()
        return render_template('import2.html', form=import_form)
    elif import_form.submit.data:
        if import_form.validate():
            books = import_form.books.entries
            for book in books:
                new_book = Book(isbn=book.isbn.data, author=book.author.data, title=book.title.data,
                                date=book.date.data, pages=book.pages.data, url=book.url.data,
                                language=book.language.data)
                db.session.add(new_book)
                db.session.commit()
            return redirect(url_for('books.show_books'))
        return render_template('import2.html', form=import_form)
    else:
        url = 'https://www.googleapis.com/books/v1/volumes?' + query
        books = get_request(url)
        if books:
            for book in books:
                if book['date']:
                    new_date = fix_date(book['date'])
                    book['date'] = datetime.strptime(
                        new_date, '%Y-%m-%d').date()
                import_form.books.append_entry(book)
            return render_template('import2.html', form=import_form)
        else:
            return redirect(url_for('books'))
