import os
import unittest
import warnings
from src.forms import BaseBookForm, BaseFilterForm, BaseSearchForm
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
        book = BaseBookForm()
        self.assertFalse(book.validate())
        errors = book.errors.items()
        self.assertIn(('isbn', ['This field is required.']), errors)
        self.assertIn(('title', ['This field is required.']), errors)
        self.assertIn(('author', ['This field is required.']), errors)

    def test_book_with_isbn(self):
        book = BaseBookForm(isbn="9788320717501")
        self.assertFalse(book.validate())
        errors = book.errors.items()
        self.assertIn(('title', ['This field is required.']), errors)
        self.assertIn(('author', ['This field is required.']), errors)

    def test_book_with_title_isbn(self):
        book = BaseBookForm(isbn="9788320717501", title="Miguel de Cervantes")
        self.assertFalse(book.validate())
        errors = book.errors.items()
        self.assertIn(('author', ['This field is required.']), errors)

    def test_good_book(self):
        book = BaseBookForm(isbn="9788320717501",
                            title="Miguel de Cervantes", author="Miguel de Cervantes")
        self.assertTrue(book.validate())

    def test_wrong_isbn(self):
        book = BaseBookForm(isbn="97883207175ad",
                            title="Miguel de Cervantes", author="Miguel de Cervantes")
        self.assertFalse(book.validate())
        errors = book.errors.items()
        self.assertIn(('isbn', ['Invalid input.']), errors)

    def test_wrong_url(self):
        book = BaseBookForm(isbn="9788320717501",
                            title="Miguel de Cervantes", author="Miguel de Cervantes", url="wrong")
        self.assertFalse(book.validate())
        errors = book.errors.items()
        self.assertIn(('url', ['Invalid URL.']), errors)

    def test_filter_form(self):
        filter = BaseFilterForm(startdate_field="2021-07-12",
                                enddate_field="2021-07-05")
        self.assertFalse(filter.validate())
        errors = filter.errors.items()
        self.assertIn(
            ('enddate_field', ["End date must not be earlier than start date."]), errors)

    def test_filter_form_good(self):
        filter = BaseFilterForm(enddate_field="2021-07-12",
                                startdate_field="2021-07-05")
        self.assertTrue(filter.validate())

    def test_filter_optional(self):
        filter = BaseFilterForm()
        self.assertTrue(filter.validate())

    def test_wrong_isbn(self):
        search = BaseSearchForm(isbn="97883207175ab")
        self.assertFalse(search.validate())
        errors = search.errors.items()
        self.assertIn(('isbn', ['Invalid input.']), errors)

    def test_search_empty(self):
        filter = BaseSearchForm()
        self.assertTrue(filter.validate())

    def tearDown(self):
        os.remove(DATABASE_PATH + TEST_DB)
