from flask_testing import TestCase
from app import app, app_config
import json
from app.api.views.user_views import users_list, meals_list, menu_list, order_list


class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        """
        app.config.from_object(app_config["testing"])
        return app

    def setUp(self):
        self.client = app.test_client(self)

    def tearDown(self):
        """
        Drop the data structure data
        """
        users_list[:] = []
        meals_list[:] = []
        menu_list[:] = []
        order_list[:] = []

    def register_user(self):
        """
        Method for registering a user with dummy data
        """
        return self.client.post(
            'api/v1/auth/signup',
            data=json.dumps(dict(
                name="mariam",
                email="marie@live.com",
                password="magic",
                is_admin="True"
            )
            ),
            content_type='application/json'
        )

    def login_user(self):
        """
        Method for logging a user with dummy data
        """
        self.register_user()
        return self.client.post(
            'api/v1/auth/login',
            data=json.dumps(
                dict(
                    email="marie@live.com",
                    password="magic"
                )
            ),
            content_type='application/json'
        )

    def get_token(self):
        """
        Returns a user token
        """
        response = self.login_user()
        data = json.loads(response.data.decode())
        return data['token']

    def add_meal(self):
        """
        Function to create a meal
        """
        token = self.get_token()
        return self.client.post(
            'api/v1/meals',
            data=json.dumps(
                dict(
                    meal_name="beef and rice",
                    price="15000"
                )
            ),
            content_type='application/json',
            headers=({"token": token})
        )
    
    def get_meals(self):
        """
        function to return meals
        """
        self.add_meal()
        token = self.get_token()
        return self.client.get('api/v1/meals', headers=({"token": token}))

    def get_id(self):
        res = self.get_meals()
        id = json.loads(res.data.decode())['meals_items'][0]['id']
        return id

    def delete_meal(self):
        """
        function to delete a meal
        """
        id = self.get_id()
        token = self.get_token()
        return self.client.delete('api/v1/meals/' + id, headers=({
            "token": token
            }))

    def put_meal(self):
        """
        function to edit a meal
        """
        id = self.get_id()
        token = self.get_token()
        return self.client.put('api/v1/meals/'+id,
                               data=json.dumps(dict(
                                   meal_name="beans and rice",
                                   price="15000")),
                                   content_type='application/json',
                                   headers=({"token": token}))


    def add_menu(self):
        """
        function to create a menu
        """
        id = self.get_id()
        token = self.get_token()
        return self.client.post(
            'api/v1/menu/' + id,
            content_type='application/json', headers=({"token": token}))


    def get_menu(self):
        """
        function to return the menu
        """
        self.add_menu()
        token = self.get_token()
        return self.client.get('api/v1/menu', headers=({"token": token}))


    def add_order(self):
        """
        function to make an order
        """
        self.get_menu()
        id = self.get_id()
        token = self.get_token()
        return self.client.post('api/v1/orders/'+id, headers=({
            "token": token
        }))

    def get_orders(self):
        """
        function to return orders for authenticated admin
        """
        self.add_order()
        token = self.get_token()
        return self.client.get('api/v1/orders', headers=({"token": token}))

    def get_user_orders(self):
        """
        function to return all orders for a customer
        """
        self.add_order()
        token = self.get_token()
        return self.client.get('api/v1/user/orders', headers=({
            "token": token
        }))

    