import os
import unittest
import json
from app import create_app

config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)


class Test_auth(unittest.TestCase):
    client = app.test_client

    # def setup(self):
    # config_name = os.getenv('FLASK_CONFIG', 'development')

    # self.client = app.test_client

    def test_signup(self):
        response = self.client().post(
            'api/v1/auth/signup',
            data=json.dumps(
                dict(
                    name="mariam",
                    email="marie@live.com",
                    password="magic", confirm_password="magic")
            )
            # content_type="application/json"
        )
        # convert byte data to json or dictionary
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get('message'), "signup successful")
        # Add the same user and see...
        response = self.client().post(
            'api/v1/auth/signup',
            data=json.dumps(
                dict(
                    name="mariam",
                    email="marie@live.com",
                    password="magic", confirm_password="magic")
            )
            # content_type="application/json"
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('message'), "user already exists")
