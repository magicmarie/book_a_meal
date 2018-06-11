from tests.base import BaseTestCase
from api.models import Menu
import json


class Test_menu_options(BaseTestCase):
    def test_add_menu(self):
        """
        Test that an authenticated admin can add a meal to the menu
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "fries", 15000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            response = self.add_menu(id, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Meal successfully added to menu",
                          data.get('message'))

    def test_add_existing_meal(self):
        """
        Test an authenticated admin can not add existing meal to the menu
        """
        with self.client:
            self.register_user("marie", "marie@live.com", "marie", "True")
            token = self.get_token()
            self.add_meal(token, "fries", 15000)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
            self.add_menu(id, token)
            response = self.add_menu(id, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 409)
            self.assertIn("Meal already exists in menu",data.get('message'))
