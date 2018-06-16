from tests.base import BaseTestCase
import json


class Test_order_options(BaseTestCase):
    def test_get_orders(self):
        """
        Test that an authenticated admin can get all orders made from his meals
        """
        self.add_order()
        response = self.get_orders()
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('status'), "success")

    def test_get_user_orders(self):
        """
        Test that an authenticated user can get his orders
        """
        response = self.get_user_orders()
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('status'), "success")

    def test_post_orders(self):
        """
        Test that an authenticated user can make an order
        """
        response = self.add_order()
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get('message'), "Order sent successfully")
