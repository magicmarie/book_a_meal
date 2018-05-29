from tests.base import BaseTestCase
from api.models import Meal
import json


class Test_meal_options(BaseTestCase):
    def test_add_meal(self):
        """
        Test that an authenticated admin can add a meal
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            response = self.add_meal(token, "pilawo", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "Meal successfully created")

    def test_missing_meal_name_details(self):
        """
        Test that the meal_name details are set when sending request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            response = self.add_meal(token, "", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "invalid, Enter meal name please")
            self.assertEqual(response.status_code, 400)

    def test_invalid_name_details(self):
        """
        Test that the meal name details are valid characters when sending request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            response = self.add_meal(token, "@#$%&*", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Invalid characters not allowed")
            self.assertEqual(response.status_code, 401)

    def test_token_missing(self):
        """
        Test for token when sending request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            response = self.add_meal("", "pilawo", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_meal_name_already_exists(self):
        """
        Test that the meal name already exists.
        """

        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            response = self.add_meal(token, "fries", 10000)
            response = self.add_meal(token, "fries", 10000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Meal name already exists")
            self.assertEqual(response.status_code, 400)

    def test_invalid_admin(self):
        """
        Test invalid admin.
        """

        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "False")
            token = self.get_token()
            response = self.add_meal(token, "fries", 10000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Customer is not authorized to create meals")
            self.assertEqual(response.status_code, 401)


