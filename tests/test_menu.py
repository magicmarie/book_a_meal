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

    def test_add_existing_meal_to_menu(self):
        """
        Test that an authenticated admin can't add existing meal to the menu
        """
        with self.client:
            self.add_menu()
            self.add_meal()
            response = self.client.post('api/v1/auth/login', 
            data=json.dumps(dict(
                                    email="marie@live.com",
                                    password="magic"
                                )
                            ),
                            content_type='application/json'
                        )
            token = json.loads(response.data.decode())['token']
            id = self.get_id()
            res = self.client.post('api/v1/menu/' + id,
            content_type='application/json', headers=({"token": token}))
            data1 = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 409)
            self.assertEqual(data1.get('message'),
                             "Meal already exists in menu")

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
