from tests.base import BaseTestCase
from api.models import User
from api import DB
import unittest
import json


class Test_auth(BaseTestCase):
    def test_signup(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.register_user()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('status'), "success")
            self.assertEqual(data.get('message'), "User successfully created")
            self.assertEqual(response.content_type, 'application/json')
