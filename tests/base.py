from flask_testing import TestCase
from app import app, app_config
import json
from app.api.views import users_list, meals_list, menu_list, order_list


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object(app_config["testing"])
        return app

    def setUp(self):


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
                confirm_password="magic",
                isAdmin="true"
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

    def add_meal(self):
        return self.client.post(
            'api/v1/meals',
            data=json.dumps(
                dict(
                    meal_name="beef and rice",
                    price="15000"
                )
            ),
            content_type='application/json'
        )

    def add_menu(self):
        return self.client.post(
            'api/v1/menu',
            data=json.dumps(
                dict(
                    menu_name="Monday"
                )
            ),
            content_type='application/json'
        )

    def delete_meal(self):
        return self.client.delete(
            'api/vi/<meal_id>'
        )

    def get_meals(self):
        return self.client.get('api/v1/meals',
                               content_type='application/json'
                               )
