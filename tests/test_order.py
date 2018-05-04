from tests.base import BaseTestCase
import json


class Test_order_options(BaseTestCase):
    def test_get_orders(self):
        self.register_user()
        token = self.get_token()
        self.add_meal(token)
        result = json.loads(self.get_meals(token).data.decode())
        print(result)
        id = result['meals_items'][0]['id']
        self.add_menu(id, token)
        self.add_order(id, token)
        response = self.get_orders(token)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('message'), "Order sent successfully")

    def test_post_orders(self):
        self.register_user()
        token = self.get_token()
        self.add_meal(token)
        result = json.loads(self.get_meals(token).data.decode())
        id = result['meals_items'][0]['id']
        self.add_menu(id, token)
        response = self.add_order(id, token)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get('message'), "Order sent successfully")
