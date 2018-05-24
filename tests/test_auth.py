from tests.base import BaseTestCase
import unittest
from api.models import User
from api import DB
import json


class Test_auth(BaseTestCase):
    def test_signup(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.register_user(
                "marie", "marie@gmail.com", "marie", True)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('status'), "success")
            self.assertEqual(data.get('message'), "User successfully created")
            self.assertEqual(response.content_type, 'application/json')

    def test_missing_name_details(self):
        """
        Test that the name details are set when sending request
        """
        with self.client:
            response = self.register_user("", "marie@live.com", "marie", True)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "invalid, Enter name please")
            self.assertEqual(response.status_code, 401)

    def test_invalid_name_details(self):
        """
        Test that the name details are valid characters when sending request
        """
        with self.client:
            response = self.register_user(
                "@#$%&", "marie@live.com", "marie", True)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Invalid characters not allowed")

    def test_missing_password_details(self):
        """
        Test that the password details are set when sending request
        """
        with self.client:
            response = self.register_user("name", "marie@live.com", "", True)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Enter password")
            self.assertEqual(response.status_code, 401)

    def test_short_password_details(self):
        """
        Test that the password details are set right when sending request
        """
        with self.client:
            response = self.register_user(
                "name", "marie@live.com", "mari", True)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Password is too short, < 5")
            self.assertEqual(response.status_code, 401)

    def test_valid_email(self):
        """
        Test that the email details are valid when sending request
        """
        with self.client:
            response = self.register_user(
                "name", "marielive.com", "marie", True)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Enter valid email")
            self.assertEqual(response.status_code, 401)

    def test_user_already_registered_with_email(self):
        """
        Test that the user already exists with similar email.
        """
        user = User("marie", "marie@gmail.com", "marie", True)
        DB.session.add(user)
        DB.session.commit()

        with self.client:
            response = self.register_user(
                "marie", "marie@gmail.com", "marie", True)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Email in use already")
            self.assertEqual(response.status_code, 400)
