import re
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Date, String

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "book"
    isbn = Column(String, primary_key=True)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=True)
    pages = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    language = Column(String, nullable=True)

    @validates('isbn')
    def validate_isbn(self, key, isbn):
        assert re.match(r"^([A-Z]+:)?\d*$", isbn)
        return isbn

    @validates('url')
    def validate_url(self, key, url):
        if url:
            assert re.match(
                r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$", url)
            return url
        return url

    @property
    def serialize(self):
        return {
            "isbn": self.isbn,
            "author": self.author,
            "title": self.title,
            "date": self.date.isoformat() if self.date else None,
            "url": self.url,
            "lang": self.language
        }
