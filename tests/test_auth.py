"""test auth"""
import json
from tests.base import BaseTestCase


class TestAuth(BaseTestCase):
    """class Test_auth"""
    def test_signup(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.register_user()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "User successfully created")

    def test_existing_user(self):
        """
        Test an existing email can't be reused through the api
        """
        with self.client:
            self.register_user()
            res = self.register_user()
            data1 = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 409)
            self.assertEqual(data1.get('message'), "email already in use")

    def test_login(self):
        """
        Test a registered user  is logged in successfully through the api
        """
        with self.client:
            response = self.login_user()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data.get('message'),
                             "User logged in successfully")
