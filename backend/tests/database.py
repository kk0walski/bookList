import os
import warnings
import datetime
from src.app import create_app
from flask_testing import TestCase
from src.model import Book, db

PROJECT_PATH, _ = os.path.split(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = PROJECT_PATH + '/src/'
TEST_DB = "test.db"


class TestDatabase(TestCase):

    render_templates = True

    def create_app(self):

        warnings.simplefilter('ignore', category=DeprecationWarning)
        app = create_app(
            {"SQLALCHEMY_DATABASE_URI": f"sqlite:///{TEST_DB}", "TESTING": True}
        )
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_database(self):
        book = Book(title="Don Quixote", author="Miguel de Cervantes", date=datetime.date(2012, 11, 10),
                    isbn="9788320717501",
                    pages=100,
                    language='polish',
                    url="https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/don_quixote.jpg"
                    )
        db.session.add(book)
        db.session.commit()

        assert db.session.query(Book).count() == 1

    def tearDown(self):
        os.remove(DATABASE_PATH + TEST_DB)
