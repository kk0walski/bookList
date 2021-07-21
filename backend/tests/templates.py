import warnings
from src.app import create_app
from flask_testing import TestCase


TEST_DB = "test.db"


class TestNotRenderTemplates(TestCase):

    render_templates = False

    def create_app(self):

        warnings.simplefilter('ignore', category=DeprecationWarning)
        app = create_app(
            {"SQLALCHEMY_DATABASE_URI": f"sqlite:///{TEST_DB}", "TESTING": True}
        )
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_index(self):
        response = self.client.get("/")
        self.assert_template_used('index.html')

    def test_books(self):
        response = self.client.get("/books/")
        self.assert_template_used('books.html')

    def test_book(self):
        response = self.client.get("/books/add")
        self.assert_template_used('book.html')

    def test_import(self):
        response = self.client.get("/import/")
        self.assert_template_used('import.html')
