from tests.base import BaseTestCase
import unittest
from api.models.user import User
from api import DB
import json


class Test_auth(BaseTestCase):
    def test_signup(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.register_user(
                "marie", "marie@gmail.com", "marie", "True")
            self.assertEqual(response.status_code, 201)

    def test_missing_name_details(self):
        """
        Test that the name details are set when sending request
        """
        with self.client:
            response = self.register_user(
                "", "marie@live.com", "marie", "True")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Enter name with more than 2 characters")
            self.assertEqual(response.status_code, 400)

    def test_long_name_details(self):
        """
        Test that the name details are not too long when sending request
        """
        with self.client:
            response = self.register_user(
                "qwertyuiopljkhgfdsazxcvbnmmagicmarie",
                "marie@live.com", "marie", "True")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Enter name with less than 25 characters")
            self.assertEqual(response.status_code, 400)

    def test_invalid_name_details(self):
        """
        Test that the name details are valid characters when sending request
        """
        with self.client:
            response = self.register_user(
                "@#$%&", "marie@live.com", "marie", "True")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Invalid characters not allowed")
            self.assertEqual(response.status_code, 400)

    def test_missing_password_details(self):
        """
        Test that the password details are set when sending request
        """
        with self.client:
            response = self.register_user("name", "marie@live.com", "", "True")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Enter password")
            self.assertEqual(response.status_code, 400)

    def test_short_password_details(self):
        """
        Test that the password details are set right when sending request
        """
        with self.client:
            response = self.register_user(
                "name", "marie@live.com", "mari", "True")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Enter password with more than 4 characters")
            self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        """
        Test that the email details are valid when sending request
        """
        with self.client:
            response = self.register_user(
                "marie", "marielive.com", "marie", "True")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Enter valid email")
            self.assertEqual(response.status_code, 400)

    def test_user_already_registered_with_email(self):
        """
        Test that the user already exists with similar email.
        """
        user = User("marie", "marie@gmail.com", "marie", "True")
        DB.session.add(user)
        DB.session.commit()

        with self.client:
            response = self.register_user(
                "marie", "marie@gmail.com", "marie", "True")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "email already in use")
            self.assertEqual(response.status_code, 409)

    def test_login_unknown_user(self):
        """
        Test a user with invalid login details
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            response = self.login_user("mariam@live.com", "marie")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'),
                             "User does not exist")

    def test_login_wrong_password(self):
        """
        Test a user with invalid login details
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            response = self.login_user("marie@live.com", "maries")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'),
                             "wrong password or email credentials")

    def test_login(self):
        """
        Test a registered user  is logged in successfully through the api
        """
        with self.client:
            response = self.login_user("marie@live.com", "marie")
            self.assertEqual(response.status_code, 200)
