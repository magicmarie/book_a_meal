from tests.base import BaseTestCase
from api.models import Menu
import json


class Test_menu_options(BaseTestCase):
    def test_add_menu(self):
        """
        Test that an authenticated admin can add a meal to the menu
        """
        with self.client:
            response = self.add_menu()
            self.assertEqual(response.status_code, 200)

    def test_add_existing_meal(self):
        """
        Test an authenticated admin can not add existing meal to the menu
        """
        with self.client:
            self.add_menu()
            token = self.get_token()
            id = self.get_id()
            response = self.client.post(
            'api/v1/menu/{}'.format(id),
            content_type='application/json', headers=({"token": token}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 409)

    def test_token_missing_add_menu(self):
        """
        Test for token when sending add menu request
        """
        with self.client:
            id = self.get_id()
            response = self.client.post(
            'api/v1/menu/{}'.format(id),
            content_type='application/json', headers=({"token": ""}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_invalid_token_add_menu(self):
        """
        Test for valid token when sending add menurequest
        """
        with self.client:
            id = self.get_id()
            response = self.client.post('api/v1/menu/{}'.format(id),
            content_type='application/json', headers=({"token": "12345"}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

    def test_none_admin_add_menu(self):
        """
        Test none admin on adding meals to a menu
        """

        with self.client:
            token = self.customer()
            id = self.get_id()
            response = self.client.post('api/v1/menu/{}'.format(id),
            content_type='application/json', headers=({"token": token}))
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Customer is not allowed to do this")
            self.assertEqual(response.status_code, 401)

    def test_non_existent_meal(self):
        """
        Test none existent meal 
        """

        with self.client:
            self.get_meals()
            id = 100
            token = self.get_token()
            response = self.client.post('api/v1/menu/{}'.format(id), headers=({
                            "token": token
                        }))
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Meal not found")
            self.assertEqual(response.status_code, 404)
