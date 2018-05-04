from tests.base import BaseTestCase
import json


class Test_meal_options(BaseTestCase):
    def test_add_meal(self):
        with self.client:
            self.register_user()
            token = self.get_token()
            response = self.add_meal(token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "Meal successfully created")
            # Add the same meal and see...
            res = self.add_meal(self.get_token())
            data1 = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data1.get('message'), "Meal name already exists")

    def test_get_meals(self):
        with self.client:
            self.register_user()
            token = self.get_token()
            self.add_meal(token)
            response = self.get_meals(token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(u"beef and rice",
                          data['meals_items'][0]['meal_name'])

    def test_delete_meal(self):
        with self.client:
            self.register_user()
            token = self.get_token()
            self.add_meal(token)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())[
                'meals_items'][0]['id']
            response = self.delete_meal(id, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Meal deleted succesfully", data)

    def test_put_meal(self):
        with self.client:
            self.register_user()
            token = self.get_token()
            self.add_meal(token)
            get_meal = self.get_meals(token)
            id = json.loads(get_meal.data.decode())[
                'meals_items'][0]['id']
            response = self.put_meal(id, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("Meal updated successfully", data.get('message'))
