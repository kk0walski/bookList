from flask import Blueprint, render_template, redirect, url_for
from .forms import FilterForm, BookFormSubmit
from .model import Book, db

static = Blueprint("static", __name__)
books = Blueprint('books', __name__,  url_prefix="/books")


@static.route('/')
def index():
    return render_template('index.html')


@books.route('/edit/<string:isbn>', methods=["PUT", "GET"])
def book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    form = BookFormSubmit(obj=book)
    if form.validate_on_submit():
        new_book = Book(isbn=form.isbn.data, author=form.author.data, title=form.title.data,
                        date=form.pubDate.data, pages=form.pages.data, url=form.url.data,
                        language=form.language.data)
        db.session.add(new_book)
        db.session.commit()
        return render_template('book.html', form=form)
    return render_template('book.html', form=form)


@books.route('/add', methods=["POST", "GET"])
def add_book():
    form = BookFormSubmit()
    if form.validate_on_submit():
        book = Book(isbn=form.isbn.data, author=form.author.data, title=form.title.data,
                    date=form.pubDate.data, pages=form.pages.data, url=form.url.data,
                    language=form.language.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.show_books'))
    return render_template('book.html', form=form)


@books.route('/', methods=['GET', 'POST'])
def show_books():
    form = FilterForm()
    if form.validate_on_submit():
        query_data = {
            'title': form.title.data,
            'author': form.author.data,
            'language': form.language.data,
            'date_from': form.startdate_field.data,
            'date_to': form.enddate_field.data,
        }
        return render_template('books.html', form=form, books=all_books())
    return render_template('books.html', form=form, books=all_books())


def all_books():
    books = Book.query.all()
    return books
