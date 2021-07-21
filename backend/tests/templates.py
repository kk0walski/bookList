import os
import warnings
from src.app import create_app
from flask_testing import TestCase

PROJECT_PATH, _ = os.path.split(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = PROJECT_PATH + '/src/'
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
        self.assert200(response)

    def test_books(self):
        response = self.client.get("/books/")
        self.assert_template_used('books.html')
        self.assert200(response)

    def test_book(self):
        response = self.client.get("/books/add")
        self.assert_template_used('book.html')
        self.assert200(response)

    def test_import(self):
        response = self.client.get("/import/")
        self.assert_template_used('import.html')
        self.assert200(response)

    def test_api(self):
        response = self.client.get("/api/books")
        self.assertEquals(response.json, {})

    def tearDown(self):
        os.remove(DATABASE_PATH + TEST_DB)
