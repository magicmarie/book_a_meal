"""test meals"""
import json
from tests.base import BaseTestCase


class TestMealOptions(BaseTestCase):
    """class test meal options"""

    def test_add_meal(self):
        """
        Test that an authenticated admin can add a meal
        """
        with self.client:
            response = self.add_meal()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "Meal successfully created")

    def test_add_existing_meal(self):
        """
        Test that an authenticated admin can't add an existing meal
        """
        with self.client:
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
            res = self.client.post('api/v1/meals', data=json.dumps(dict(
                                meal_name="beef and rice",
                                price="15000"
                            )
                        ),
                        content_type='application/json',
                        headers=({"token": token})
                    )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 409)
            self.assertEqual(data.get('message'), "Meal name already exists")

    def test_get_meals(self):
        """
        Test that an authenticated admin can get all his meals
        """
        with self.client:
            response = self.get_meals()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(u"beef and rice",
                          data['meals_items'][0]['meal_name'])

    def test_delete_meal(self):
        """
        Test that an authenticated admin can delete a meal
        """
        with self.client:
            self.get_id()
            response = self.delete_meal()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Meal deleted succesfully", data.get('message'))

    def test_put_meal(self):
        """
        Test that an authenticated admin can edit meal details
        """
        with self.client:
            self.get_id()
            response = self.put_meal()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("Meal updated successfully", data.get('message'))
