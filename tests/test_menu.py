from tests.base import BaseTestCase
import json


class Test_menu_options(BaseTestCase):
    def test_add_menu(self):
        with self.client:
            self.register_user()
            token = self.get_token()
            self.add_meal(token)
            result = json.loads(self.get_meals(token).data.decode())
            id = result['meals_items'][0]['id']
            response = self.add_menu(id, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Meal successfully added to menu",
                          data.get('message'))
            # Add the same menu and see...
            res = self.add_menu(id, token)
            data1 = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 409)
            self.assertEqual(data1.get('message'),
                             "Meal already exists in menu")

    def test_get_menu(self):
        with self.client:
            self.register_user()
            token = self.get_token()
            self.add_meal(token)
            result = json.loads(self.get_meals(token).data.decode())
            id = result['meals_items'][0]['id']
            self.add_menu(id, token)
            response = self.get_menu(token)
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(u"beef and rice",
                          data['menu'][0]['meal_name'])
