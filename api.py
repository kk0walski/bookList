from flask import Flask, render_template
from forms import SearchForm
from config import Config
from urllib.parse import urlencode
import json
import requests

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', books=get_books())


def map_book(book):
    return {
        'title': book.get('volumeInfo', {}).get('title', 'no_title'),
        'author': ', '.join(book.get('volumeInfo', {}).get('authors', ['annonymous'])),
        'date': book.get('volumeInfo', {}).get('publishedDate', 'no-date'),
        'isbn': book.get('volumeInfo', {}).get('industryIdentifiers', [{'identifier': "0000000000"}])[0].get('identifier'),
        'pages': book.get('volumeInfo', {}).get('pageCount', 0),
        'language': book.get('volumeInfo', {}).get('language', 'no-lang'),
        'frontPage': book.get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail', '...')
    }


def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data['items']
        reasult = map(map_book, items)
        return reasult


@app.route('/import', methods=['GET', 'POST'])
def import_books():
    form = SearchForm()
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
        return render_template('import.html', form=form, books=books)
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
