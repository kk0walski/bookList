import warnings
import urllib.request
from src.app import create_app
from flask_testing import LiveServerTestCase


TEST_DB = "test.db"


class MyTest(LiveServerTestCase):

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
