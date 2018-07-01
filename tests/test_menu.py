from tests.base import BaseTestCase
import json


class Test_menu_options(BaseTestCase):
    def test_add_menu(self):
        """
        Test that an authenticated admin can add a meal to the menu
        """
        with self.client:
            response = self.add_menu()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Meal successfully added to menu",
                          data.get('message'))

    def test_get_menu(self):
        """
        Test that an authenticated user can view the menu
        """
        with self.client:
            response = self.get_menu()
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(u"beef and rice",
                          data['menu'][0]['meal_name'])
