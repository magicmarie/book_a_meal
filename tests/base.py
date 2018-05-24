from flask_testing import TestCase
from api import APP, DB
from config import app_config
import json


class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        """
        APP.config.from_object(app_config["testing"])
        return APP

    def setUp(self):
        """
        Create the database and commits any changes made permanently
        """
        self.client = APP.test_client(self)
        DB.create_all()
        DB.session.commit()

    def tearDown(self):
        """
        Drop the database data and remove session
        """
        DB.session.remove()
        DB.drop_all()

    def register_user(self, name, email, password, isAdmin):
        """
        Method for registering a user with dummy data
        """
        return self.client.post(
            'api/v1/auth/signup',
            data=json.dumps(dict(
                name=name,
                email=email,
                password=password,
                isAdmin=isAdmin
            )
            ),
            content_type='application/json'
        )
