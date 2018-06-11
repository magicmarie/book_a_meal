from tests.base import BaseTestCase
import json



class Test_order_options(BaseTestCase):
    def test_post_orders(self):
        """
        Test that an authenticated user can make an order
        """
        self.register_user("marie", "marie@live.com", "marie", "True")
        token = self.get_token()
        self.add_meal(token, "pilawo", 15000)
        get_meal = self.get_meals(token)
        id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
        self.add_menu(id, token)
        response = self.add_order(id, token)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get('message'), "Order sent successfully")

    def test_get_orders(self):
        """
        Test that an authenticated admin can get all orders made from his meals
        """
        self.register_user("marie", "marie@live.com", "marie", "True")
        token = self.get_token()
        self.add_meal(token, "pilawo", 15000)
        get_meal = self.get_meals(token)
        id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
        self.add_menu(id, token)
        self.add_order(id, token)
        response = self.get_orders(token)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['order_items'][0]['mealId'], 1)

    def test_get_user_orders(self):
        """
        Test that an authenticated user can get his orders
        """
        self.register_user("marie", "marie@live.com", "marie", "True")
        token = self.get_token()
        self.add_meal(token, "pilawo",15000)
        get_meal = self.get_meals(token)
        id = json.loads(get_meal.data.decode())['meal_items'][0]['id']
        self.add_menu(id, token)
        self.add_order(id, token)
        response = self.get_user_orders(id, token)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('status'), "success")

    
