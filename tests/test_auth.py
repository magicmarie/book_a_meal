from tests.base import BaseTestCase
import json


class Test_auth(BaseTestCase):
    def test_signup(self):
        with self.client:
            response = self.register_user()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "User successfully created")
            # Add the same user and see...
            response = self.register_user()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "email already in use")

    def test_login(self):
        with self.client:
            self.register_user()
            response = self.login_user()
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data.get('message'),
                             "User logged in successfully")
