import os
from flask import Flask

from .routes import static, books


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
    app.register_blueprint(books)
    return app


def run():
    app = create_app()
    app.run()


if __name__ == "__main__":
    run()
