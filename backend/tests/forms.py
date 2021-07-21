import os
import unittest
import warnings
from src.forms import BookForm, BookFormSubmit, SearchForm, FilterForm
from src.app import create_app

PROJECT_PATH, _ = os.path.split(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = PROJECT_PATH + '/src/'
TEST_DB = "test.db"


class TestForms(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=DeprecationWarning)
        self.app = create_app(
            {"SQLALCHEMY_DATABASE_URI": f"sqlite:///{TEST_DB}", "TESTING": True}
        )
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_book_empty(self):
        book = BookForm()
        self.assertFalse(book.validate())
        errors = book.errors.items()
        self.assertIn(('isbn', ['This field is required.']), errors)
        self.assertIn(('title', ['This field is required.']), errors)
        self.assertIn(('author', ['This field is required.']), errors)

    def test_book_with_isbn(self):
        book = BookForm(isbn="9788320717501")
        self.assertFalse(book.validate())
        errors = book.errors.items()
        self.assertIn(('title', ['This field is required.']), errors)
        self.assertIn(('author', ['This field is required.']), errors)

    def test_book_with_title_isbn(self):
        book = BookForm(isbn="9788320717501", title="Miguel de Cervantes")
        self.assertFalse(book.validate())
        errors = book.errors.items()
        self.assertIn(('author', ['This field is required.']), errors)

    def test_good_book(self):
        book = BookForm(isbn="9788320717501",
                        title="Miguel de Cervantes", author="Miguel de Cervantes")
        self.assertTrue(book.validate())

    def tearDown(self):
        os.remove(DATABASE_PATH + TEST_DB)
