from flask_testing import TestCase
from app import app, app_config
import json
from app.api.views.user_views import users_list, meals_list, menu_list, order_list


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object(app_config["testing"])
        return app

    def setUp(self):
        self.client = app.test_client(self)

    def tearDown(self):
        users_list[:] = []
        meals_list[:] = []
        menu_list[:] = []
        order_list[:] = []

    def register_user(self):
        return self.client.post(
            'api/v1/auth/signup',
            data=json.dumps(dict(
                name="mariam",
                email="marie@live.com",
                password="magic",
                isAdmin="True"
            )
            ),
            content_type='application/json'
        )

    def login_user(self):
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
        response = self.login_user()
        data = json.loads(response.data.decode())
        return data['token']

    def add_meal(self, token):
        return self.client.post(
            'api/v1/meals',
            data=json.dumps(
                dict(
                    meal_name="beef and rice",
                    price="15000"
                )
            ),
            content_type='application/json',
            headers=dict(token=token)
        )

    def add_order(self, id, token):
        return self.client.post('api/v1/orders/'+id, headers=({"token": token}))

    def get_orders(self, token):
        return self.client.get('api/v1/orders', headers=({"token": token}))

    def add_menu(self, id, token):
        return self.client.post(
            'api/v1/menu/' + id,
            content_type='application/json', headers=({"token": token}))

    def delete_meal(self, id, token):
        return self.client.delete('api/v1/meals/' + id, headers=({"token": token}))

    def get_meals(self, token):
        return self.client.get('api/v1/meals', headers=({"token": token}))

    def put_meal(self, id, token):
        return self.client.put('api/v1/meals/'+id,
                               data=json.dumps(dict(
                                   meal_name="beans and rice",
                                   price="15000")), content_type='application/json', headers=({"token": token}))

    def get_menu(self, token):
        return self.client.get('api/v1/menu', headers=({"token": token}))
