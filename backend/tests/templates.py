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

    def test_assert_mytemplate_used(self):
        response = self.client.get("/")

        self.assert_template_used('index.html')
