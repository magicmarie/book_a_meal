from tests.base import BaseTestCase
from api.models.meal import Meal
import json


class Test_meal_options(BaseTestCase):
    def test_add_meal(self):
        """
        Test that an authenticated admin can add a meal
        """
        with self.client:
            response = self.add_meal("pilawo", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), "Meal successfully created")

    def test_missing_meal_name_details(self):
        """
        Test that the meal_name details are set when sending request
        """
        with self.client:
            response = self.add_meal("", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Enter meal name with more than 2 characters")
            self.assertEqual(response.status_code, 400)

    def test_short_meal_name_details(self):
        """
        Test that the meal_name details are set right when sending request
        """
        with self.client:
            response = self.add_meal("qwertyuioplkjhgfdsazxcvbnmqwertyu", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Enter meal name with less than 25 characters")
            self.assertEqual(response.status_code, 400)

    def test_positive_price_details(self):
        """
        Test that the price details are positive when sending request
        """
        with self.client:
            response = self.add_meal("beef", -15000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Price must be a positive number")
            self.assertEqual(response.status_code, 400)

    def test_price_details_number(self):
        """
        Test that the price details are numbers when sending request
        """
        with self.client:
            response = self.add_meal("beef", "jasmine")
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Price must be a number")
            self.assertEqual(response.status_code, 400)

    def test_invalid_name_details(self):
        """
        Test that the mealname details are valid characters when sending request
        """
        with self.client:
            response = self.add_meal("@#$%&*", 15000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Invalid characters not allowed")
            self.assertEqual(response.status_code, 400)

    def test_token_missing_post(self):
        """
        Test for token when sending post request
        """
        with self.client:
            token = ""
            response = self.client.post('api/v1/meals',data=json.dumps(
                dict(
                    meal_name="fries",
                    price=10000
                    )
                ),
                content_type='application/json',
                headers=({"token": token})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_invalid_token_post(self):
        """
        Test for valid token when sending post request
        """
        with self.client:
            token = "12345"
            response = self.client.post('api/v1/meals',data=json.dumps(
                dict(
                    meal_name="fries",
                    price=10000
                    )
                ),
                content_type='application/json',
                headers=({"token": token})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

    def test_meal_name_already_exists(self):
        """
        Test that the meal name already exists.
        """

        with self.client:
            self.add_meal( "fries", 10000)
            response = self.add_meal( "fries", 10000)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Meal name already exists")
            self.assertEqual(response.status_code, 409)

    def test_none_admin_post(self):
        """
        Test none admin on adding meal
        """
        with self.client:    
            token = self.customer()
            response = self.client.post('api/v1/meals', data=json.dumps(
                                dict(
                                    meal_name="fries",
                                    price=10000
                                )
                            ),
                            content_type='application/json',
                            headers=({"token": token})
                        )
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Customer is not authorized to access this page")
            self.assertEqual(response.status_code, 401)

    def test_get_meals(self):
        """
        Test that an authenticated admin can get all his meals
        """
        with self.client:
            self.add_meal("fries", 10000)
            response = self.get_meals()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(u"fries",
                          data['meal_items'][0]['meal_name'])

    def test_none_admin_get_all(self):
        """
        Test none admin on getting meals
        """

        with self.client:
            token = self.customer()
            response = self.client.get('api/v1/meals', headers=({"token": token}))
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Customer is not authorized to access this page")
            self.assertEqual(response.status_code, 401)

    def test_token_missing_get_all(self):
        """
        Test for token when sending get all meals request
        """
        with self.client:
            response = self.client.get('api/v1/meals', headers=({"token": ""}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_invalid_token_get_all(self):
        """
        Test for valid token when sending get all meals request
        """
        with self.client:
            response = self.client.get('api/v1/meals', headers=({"token": "12345"}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

    def test_delete_meal(self):
        """
        Test that an authenticated admin can delete a meal
        """
        with self.client:
            response = self.delete_meal()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Meal deleted succesfully", data.get('message'))

    def test_invalid_token_delete(self):
        """
        Test for valid token when sending delete request
        """
        with self.client:
            id = self.get_id()
            response = self.client.delete('api/v1/meals/{}'.format(id), headers=({
                            "token": "12345"
                        }))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

    def test_token_missing_delete(self):
        """
        Test for token when delete request
        """
        with self.client:
            id = self.get_id()
            response = self.client.delete('api/v1/meals/{}'.format(id), headers=({
                            "token": ""
                        }))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_none_admin_delete(self):
        """
        Test none admin can't delete a meal
        """

        with self.client:
            token = self.customer()
            id = 1
            response = self.client.delete('api/v1/meals/{}'.format(id), headers=({
                            "token": token
                        }))
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Customer is not authorized to access this page")
            self.assertEqual(response.status_code, 401)

    def test_wrong_admin_delete(self):
        """
        Test wrong admin on deleting a meal
        """

        with self.client:
            self.get_meals()
            id = 100
            token = self.get_token()
            response = self.client.delete('api/v1/meals/{}'.format(id), headers=({
                            "token": token
                        }))
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Meal not found")
            self.assertEqual(response.status_code, 400)

    def test_put_meal(self):
        """
        Test that an authenticated admin can edit meal details
        """
        with self.client:
            response = self.put_meal()
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("Meal updated successfully", data.get('message'))

    def test_invalid_token_put(self):
        """
        Test for valid token when sending put request
        """
        with self.client:
            id = self.get_id()
            response = self.client.put('api/v1/meals/{}'.format(id),
                               data=json.dumps(dict(
                                   meal_name="chips",
                                   price=15000
                               )),
                               content_type='application/json',
                               headers=({"token": "12345"}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Invalid token.Please login")

    def test_token_missing_edit(self):
        """
        Test for token when put request
        """
        with self.client:
            id = self.get_id()
            response = self.client.put('api/v1/meals/{}'.format(id),
                               data=json.dumps(dict(
                                   meal_name="chips",
                                   price=15000
                               )),
                               content_type='application/json',
                               headers=({"token": ""}))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data.get('message'), "Token is missing")

    def test_none_admin_edit(self):
        """
        Test none admin on editing a meal
        """

        with self.client:
            token = self.customer()
            id = 1
            response = self.client.put('api/v1/meals/{}'.format(id),
                               data=json.dumps(dict(
                                   meal_name="chips",
                                   price=15000
                               )),
                               content_type='application/json',
                               headers=({"token": token}))
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Customer is not authorized to access this page")
            self.assertEqual(response.status_code, 401)

    def test_wrong_admin_put(self):
        """
        Test wrong admin on editing a meal
        """

        with self.client:
            token = self.get_token()
            id = 4
            response = self.client.put('api/v1/meals/{}'.format(id),
                               data=json.dumps(dict(
                                   meal_name="chips",
                                   price=15000
                               )),
                               content_type='application/json',
                               headers=({"token": token}))
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), "Meal not found")
            self.assertEqual(response.status_code, 400)

    def test_invalid_name_details_put(self):
        """
        Test that the mealname details are valid characters on put request
        """
        with self.client:
            token = self.get_token()
            id = self.get_id()
            response = self.client.put('api/v1/meals/{}'.format(id),
                               data=json.dumps(dict(
                                   meal_name="@#$%",
                                   price=15000
                               )),
                               content_type='application/json',
                               headers=({"token": token}))
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'),
                             "Invalid characters not allowed")
            self.assertEqual(response.status_code, 400)
