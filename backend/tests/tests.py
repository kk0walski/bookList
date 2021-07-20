import unittest
from collections import namedtuple
import warnings
from src.forms import BookForm, BookFormSubmit, SearchForm, FilterForm
from src.app import create_app


TEST_DB = "test.db"


class TestAPI(unittest.TestCase):
    VALID_DATA = {
        "description": "test_description",
        "note": "test_note",
        "amount": 5.1,
    }

    def setUp(self):
        warnings.simplefilter('ignore', category=DeprecationWarning)
        self.app = create_app(
            {"SQLALCHEMY_DATABASE_URI": f"sqlite:///{TEST_DB}", "TESTING": True}
        )
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_links(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/import/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/books/add')
        self.assertEqual(response.status_code, 200)

    def test_book_form(self):
        book = BookForm()
        self.assertFalse(book.validate())
        errors = book.errors.items()
        self.assertIn(('isbn', ['This field is required.']), errors)
        self.assertIn(('title', ['This field is required.']), errors)
        self.assertIn(('author', ['This field is required.']), errors)
        book = BookForm(isbn="9788320717501")
        self.assertFalse(book.validate())
        self.assertIn(('title', ['This field is required.']), errors)
        self.assertIn(('author', ['This field is required.']), errors)
        book = BookForm(isbn="9788320717501", title="Miguel de Cervantes")
        self.assertFalse(book.validate())
        self.assertIn(('author', ['This field is required.']), errors)
        book = BookForm(isbn="9788320717501",
                        title="Miguel de Cervantes", author="Miguel de Cervantes")
        self.assertTrue(book.validate())

    def tearDown(self):
        pass