import os
import warnings
import urllib.request
from src.app import create_app
from flask_testing import LiveServerTestCase

PROJECT_PATH, _ = os.path.split(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = PROJECT_PATH + '/src/'
TEST_DB = "test.db"


class TestServer(LiveServerTestCase):

    def create_app(self):
        warnings.simplefilter('ignore', category=DeprecationWarning)
        app = create_app()
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def test_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def tearDown(self):
        try:
            os.remove(DATABASE_PATH + TEST_DB)
        except FileNotFoundError:
            pass
