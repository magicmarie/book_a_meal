from flask_testing import TestCase
from app import app, app_config
import json
from app.api.views import users_list


class BaseTestCase(TestCase):
    """ """

    def create_app(self):
        app.config.from_object(app_config["testing"])
        return app

    def tearDown(self):
        users_list[:] = []

    def register_user(self):
        return self.client.post(
            'api/v1/auth/signup',
            data=json.dumps(
                dict(
                    name="mariam",
                    email="marie@live.com",
                    password="magic",
                    confirm_password="magic",
                    isAdmin="true"
                )
            ),
            content_type='application/json'
        )

    def login_user(self):
        return self.client.post(
            'api/v1/auth/login',
            data=json.dumps(
                dict(
                    email="marie@live.com",
                    password="magic",
                )
            ),
            content_type='application/json'
        )


