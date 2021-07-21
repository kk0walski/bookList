import os
import datetime
import unittest
import warnings
from src.app import create_app
from src.model import Book, db
from sqlalchemy.exc import IntegrityError


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

    def test_database_key(self):
        book = Book(title="Don Quixote", author="Miguel de Cervantes", date=datetime.date(2012, 11, 10),
                    isbn="9788320717501",
                    pages=100,
                    language='fr',
                    url="https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/don_quixote.jpg"
                    )
        db.session.add(book)
        db.session.commit()

        self.assertEqual(db.session.query(Book).count(), 1)

    def test_two_same_isbns(self):
        book = Book(title="Don Quixote", author="Miguel de Cervantes", date=datetime.date(2012, 11, 10),
                    isbn="9788320717501",
                    pages=100,
                    language='fr',
                    url="https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/don_quixote.jpg"
                    )
        db.session.add(book)
        db.session.commit()

        self.assertEqual(db.session.query(Book).count(), 1)

        with self.assertRaises(IntegrityError):
            book = Book(title="As I Lay Dying", author="William Faulkner", date=datetime.date(2012, 5, 10),
                        isbn="9788320717501",
                        pages=100,
                        language='en',
                        url="https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/as_I_lay.jpg"
                        )

            db.session.add(book)
            db.session.commit()

    def tearDown(self):
        os.remove(DATABASE_PATH + TEST_DB)
