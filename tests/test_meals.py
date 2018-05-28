from tests.base import BaseTestCase
import json


class Test_meal_options(BaseTestCase):
    def test_add_meal(self):
        """
        Test that an authenticated admin can add a meal
        """
        with self.client:
            self.register_user("marie", "marie@gmail.com", "marie", True)
            token = self.get_token()
            response = self.add_meal(token, "pilawo", 15000)
            # data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "Meal successfully created")
