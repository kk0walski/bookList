import os
from flask import Flask

from .import_books import import_books
from .routes import static, books
from .api import api
from .model import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess',
        SQLALCHEMY_DATABASE_URI="sqlite:///../../books.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config:
        app.config.from_mapping(**test_config)

    app.register_blueprint(static)
    app.register_blueprint(api)
    app.register_blueprint(books)
    app.register_blueprint(import_books)

    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create sql tables for our data models
    return app

app = create_app()