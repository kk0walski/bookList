from flask import Flask, render_template
from forms import SearchForm, FilterForm
from config import Config
from urllib.parse import urlencode
import json
import requests

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FilterForm()
    if form.validate_on_submit():
        if form.validate_date_to_field(form.date_to_field.data):
            query_data = {
                'title': form.title.data,
                'author': form.author.data,
                'language': form.language.data,
                'date_from': form.date_from.data,
                'date_to': form.date_to.data,
            }
            return render_template('index.html', form=form, books=get_books())
        else:
            return render_template('index.html', form=form)
    return render_template('index.html', form=form, books=get_books())


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
            'date': book.get('volumeInfo', {}).get('publishedDate', 'no-date'),
            'pages': book.get('volumeInfo', {}).get('pageCount', 0),
            'language': book.get('volumeInfo', {}).get('language', 'no-lang'),
            'frontPage': book.get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail', '#')
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
        return [(lambda d: d.update(isbn=key) or d)(val) for (key, val) in reasult.items()]


@app.route('/import', methods=['GET', 'POST'])
def import_books():
    form = SearchForm(request.form)
    if form.validate_on_submit():
        query_data = {
            'q': form.search.data,
            'intitle': form.title.data,
            'inauthor': form.author.data,
            'inpublisher': form.publisher.data,
            'subject': form.subject.data,
            'isbn': form.subject.data,
        }
        query_data = dict(
            filter(lambda elem: elem[1] != '' or elem[0] == 'q', query_data.items()))
        querystring = urlencode(query_data)
        querystring = querystring.replace('&', '+')
        querystring = querystring.replace('=', ':')
        querystring = querystring.replace(':', '=', 1)
        if query_data['q'] == '':
            querystring = querystring.replace('+', '', 1)
        url = 'https://www.googleapis.com/books/v1/volumes?' + querystring
        books = get_request(url)
        return render_template('import.html', form=form, books=json.dumps(books))
    return render_template('import.html', form=form)


def get_books():
    books = [
        {
            'title': "Don Quixote",
            'author': "Miguel de Cervantes",
            'date': "10-11-2012",
            'isbn': "9788320717501",
            'pages': 100,
            'language': 'polish',
            'frontPage': "https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/don_quixote.jpg"
        },
        {
            'title': "As I Lay Dying",
            'author': "William Faulkner",
            'date': "10-11-2012",
            'isbn': "9788320717501",
            'pages': 100,
            'language': 'polish',
            'frontPage': "https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/as_I_lay.jpg"
        },
        {
            'title': "Things Fall Apart",
            'author': "Miguel de Cervantes",
            'date': "10-11-2012",
            'isbn': "9788320717501",
            'pages': 100,
            'language': 'polish',
            'frontPage': "https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/things_fall_apart.jpg"
        }
    ]

    return books


if __name__ == '__main__':
    app.run(debug=True)
