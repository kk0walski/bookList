import os
import warnings
import datetime
from src.app import create_app
from flask_testing import TestCase
from src.model import Book, db

PROJECT_PATH, _ = os.path.split(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = PROJECT_PATH + '/src/'
TEST_DB = "test.db"


class TestTemplates(TestCase):

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
        response = self.client.get("/api/")
        self.assertEquals(response.json, {})

    def test_filtering(self):
        app = self.create_app()
        book = dict(title="Don Quixote", author="Miguel de Cervantes", date=datetime.date(2012, 11, 10),
            isbn="9788320717501",
            pages=100,
            language='fr',
            url="https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/don_quixote.jpg"
            )
        with app.test_client() as c:
            response = self.client.post(
                "/books/add",
                data = book,
                follow_redirects=True, 
                headers = {"Content-Type":"application/x-www-form-urlencoded"}
            )
            books = db.session.query(Book).all()
            self.assertEqual(db.session.query(Book).count(), 1)
            self.assert_template_used('books.html')
            self.assertContext('books', books)
            self.assert200(response)

            query_data = {
                'title': "Hoobit",
                'author': None,
                'language': None,
                'date_from': None,
                'date_to': None,
            }
            response = self.client.get(
                "/books/",
                query_string = query_data,
                follow_redirects=True, 
                headers = {"Content-Type":"application/x-www-form-urlencoded"}
            )
            self.assert_template_used('books.html')
            self.assertContext('books', [])
            self.assert200(response)

            query_data = {
                'title': "Don",
                'author': None,
                'language': None,
                'date_from': None,
                'date_to': None,
            }
            response = self.client.get(
                "/books/",
                query_string = query_data,
                follow_redirects=True, 
                headers = {"Content-Type":"application/x-www-form-urlencoded"}
            )
            self.assert_template_used('books.html')
            self.assertContext('books', books)
            self.assert200(response)

    def test_post_wrong(self):
        app = self.create_app()
        with app.test_client() as c:
            response = self.client.post(
                "/books/add",
                data = dict(title="Don Quixote", author="Miguel de Cervantes", date=datetime.date(2012, 11, 10),
                        isbn="97883207175ab",
                        pages=100,
                        language='fr',
                        url="https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/don_quixote.jpg"
                        ),
                follow_redirects=True, 
                headers = {"Content-Type":"application/x-www-form-urlencoded"}
            )
            self.assertEqual(db.session.query(Book).count(), 0)
            self.assert_template_used('book.html')
            self.assert200(response)
            response = self.client.get('/books/')
            self.assert_template_used('books.html')
            self.assertContext('books', [])
            self.assert200(response)

    
    def tearDown(self):
        os.remove(DATABASE_PATH + TEST_DB)
