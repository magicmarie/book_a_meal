from flask_testing import TestCase
from app import app, app_config


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object(app_config["testing"])
        return app
