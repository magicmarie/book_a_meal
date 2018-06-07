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
        Test that the mealname details are valid characters when sending request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            response = self.add_meal(token, "@#$%&*", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Invalid characters not allowed")
            self.assertEqual(response.status_code, 401)

    def test_token_missing_post(self):
        """
        Test for token when sending post request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            response = self.add_meal("", "pilawo", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_invalid_token_post(self):
        """
        Test for valid token when sending post request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = "12345"
            response = self.add_meal(token, "pilawo", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

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

    def test_none_admin_post(self):
        """
        Test none admin on adding meal
        """

        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "False")
            token = self.get_token()
            response = self.add_meal(token, "fries", 10000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Customer is not authorized to create meals")
            self.assertEqual(response.status_code, 401)

    def test_get_meals(self):
        """
        Test that an authenticated admin can get all his meals
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "fries", 10000)
            response = self.get_meals(token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(u"fries",
                          data['meal_items'][0]['meal_name'])

    def test_none_admin_get_all(self):
        """
        Test none admin on getting meals
        """

        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "False")
            token = self.get_token()
            self.add_meal(token, "fries", 10000)
            response = self.get_meals(token)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Customer is not authorized to view meals")
            self.assertEqual(response.status_code, 401)

    def test_token_missing_get_all(self):
        """
        Test for token when sending get all meals request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "pilawo", 15000)
            response = self.get_meals("")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_invalid_token_get_all(self):
        """
        Test for valid token when sending get all meals request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "pilawo", 15000)
            response = self.get_meals("12345")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

    def test_delete_meal(self):
        """
        Test that an authenticated admin can delete a meal
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "pilawo", 15000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            print(id)
            response = self.delete_meal(token, id)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Meal deleted succesfully", data.get('message'))

    def test_invalid_token_delete(self):
        """
        Test for valid token when sending delete request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "pilawo", 15000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            response = self.delete_meal("12345", id)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

    def test_token_missing_delete(self):
        """
        Test for token when delete request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "pilawo", 15000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            response = self.delete_meal("", id)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_none_admin_delete(self):
        """
        Test none admin can't delete a meal
        """

        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "fries", 10000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']

            self.register_user("marie", "mariam@live.com", "marie", "False")
            token = self.get_token("mariam@live.com")
            response = self.delete_meal(token, id)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Customer is not allowed to do this")
            self.assertEqual(response.status_code, 401)

    def test_wrong_admin_delete(self):
        """
        Test wrong admin on deleting a meal
        """

        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "fries", 10000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            response = self.delete_meal(token, 7)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Meal not found")
            self.assertEqual(response.status_code, 404)

    def test_put_meal(self):
        """
        Test that an authenticated admin can edit meal details
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "fries", 10000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            response = self.put_meal(id, token, "friess", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("Meal updated successfully", data.get('message'))

    def test_invalid_token_put(self):
        """
        Test for valid token when sending put request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "pilawo", 15000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            response = self.put_meal(id, "12345", "friess", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

    def test_token_missing_edit(self):
        """
        Test for token when put request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "pilawo", 15000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            response = self.put_meal(id, "", "friess", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_none_admin_edit(self):
        """
        Test none admin on editing a meal
        """

        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "fries", 10000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']

            self.register_user("marie", "mariam@live.com", "marie", "False")
            token = self.get_token("mariam@live.com")
            response = self.put_meal(id, token, "friess", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Customer is not allowed to do this")
            self.assertEqual(response.status_code, 401)

    def test_wrong_admin_put(self):
        """
        Test wrong admin on editing a meal
        """

        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "fries", 10000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            response = self.put_meal(7, token, "friess", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Meal not found")
            self.assertEqual(response.status_code, 404)

    def test_missing_meal_name_details_put(self):
        """
        Test that the meal_name details are set on put request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "fries", 15000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            response = self.put_meal(id, token, "", 10000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "invalid, Enter meal name please")
            self.assertEqual(response.status_code, 400)

    def test_invalid_name_details_put(self):
        """
        Test that the mealname details are valid characters on put request
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "fries", 15000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            response = self.add_meal(token, "@#$%&*", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Invalid characters not allowed")
            self.assertEqual(response.status_code, 401)
