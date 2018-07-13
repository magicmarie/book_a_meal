from tests.base import BaseTestCase
import json


class Test_order_options(BaseTestCase):

    def test_get_user_orders(self):
        """
        Test that an authenticated user can get his orders
        """
        response = self.get_user_orders()
        self.assertEqual(response.status_code, 200)

    def test_get_admin_orders(self):
        """
        Test an authenticated admin  can get orders from his meals
        """
        response = self.get_admin_orders()
        self.assertEqual(response.status_code, 200)

    def test_invalid_token_post(self):
        """
        Test invalid token on post order request
        """
        with self.client:
            id = self.get_meal_id()
            menu_id = self.get_menu_id()
            response = self.client.post(
                'api/v1/orders/{}/{}'.format(menu_id, id), headers=({"token": "12345"}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

    def test_missing_token_post(self):
        """
        Test for missing token on post order request
        """
        with self.client:
            id = self.get_meal_id()
            menu_id = self.get_menu_id()
            response = self.client.post(
                'api/v1/orders/{}/{}'.format(menu_id, id), headers=({"token": ""}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_non_existent_meal_post(self):
        """
        Test authenticated cannot make an order that doesnt exist on the menu
        """
        with self.client:
            id = 100
            token = self.get_token()
            menu_id = self.get_menu_id()
            response = self.client.post(
                'api/v1/orders/{}/{}'.format(menu_id, id),
                headers=({"token": token}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], "Meal does not exist")

    def test_invalid_token_admin_get(self):
        """
        Test invalid token on get all orders by admin request
        """
        with self.client:
            response = self.client.get(
                'api/v1/orders', headers=({"token": "12345"}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

    def test_non_admin_get(self):
        """
        Test a customer can not get orders of other users
        """
        with self.client:
            token = self.customer()
            response = self.client.get(
                'api/v1/orders', headers=({"token": token}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'),
                             "Customer is not authorized to access this page")

    def test_invalid_token_customer_get(self):
        """
        Test invalid token on get all orders by customer request
        """
        with self.client:
            response = self.client.get(
                'api/v1/user/orders', headers=({"token": "12345"}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Invalid token.Please login")
