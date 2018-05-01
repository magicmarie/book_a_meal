from tests.base import BaseTestCase
import json


class Test_meal_options(BaseTestCase):
    def test_add_meal(self):
        with self.client:
            response = self.add_meal()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "Meal successfully created")
            # Add the same meal and see...
            res = self.add_meal()
            data1 = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data1.get('message'), "Meal name already exists")

    def test_get_meals(self):
        with self.client:
            response = self.add_meal()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data.get('message'), "")

    def delete_meal(self):
        with self.client:
            self.add_meal()
            response = self.delete_meal()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data.get('message'),
                             "Meal succesfully deleted")
