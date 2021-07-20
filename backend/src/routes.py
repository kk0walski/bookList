from flask import Blueprint, render_template
from .forms import FilterForm, BookFormSubmit

static = Blueprint("static", __name__)
books = Blueprint('books', __name__,  url_prefix="/books")


@static.route('/')
def index():
    return render_template('index.html')


@books.route('/edit/<string:isbn>', methods=["PUT", "GET"])
def book(isbn):
    form = BookFormSubmit()
    if form.validate_on_submit():
        return render_template('book.html', form=form)
    return render_template('book.html', form=form)


@books.route('/add', methods=["POST", "GET"])
def add_book():
    form = BookFormSubmit()
    if form.validate_on_submit():
        return render_template('book.html', form=form)
    return render_template('book.html', form=form)


@books.route('/', methods=['GET', 'POST'])
def get_books():
    form = FilterForm()
    if form.validate_on_submit():
        query_data = {
            'title': form.title.data,
            'author': form.author.data,
            'language': form.language.data,
            'date_from': form.startdate_field.data,
            'date_to': form.enddate_field.data,
        }
        return render_template('books.html', form=form, books=get_books())
    return render_template('books.html', form=form, books=get_books())


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
