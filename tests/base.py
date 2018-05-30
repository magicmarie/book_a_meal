from flask_testing import TestCase
from api import APP, DB
from config import app_config
import json


class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        """
        APP.config.from_object(app_config["testing"])
        return APP

    def setUp(self):
        """
        Create the database and commits any changes made permanently
        """
        self.client = APP.test_client(self)
        DB.create_all()
        DB.session.commit()

    def tearDown(self):
        """
        Drop the database data and remove session
        """
        DB.session.remove()
        DB.drop_all()

    def register_user(self, name, email, password, isAdmin):
        """
        Method for registering a user with dummy data
        """
        return self.client.post(
            'api/v1/auth/signup',
            data=json.dumps(dict(
                name=name,
                email=email,
                password=password,
                isAdmin=isAdmin
            )
            ),
            content_type='application/json'
        )

    def login_user(self, email, password):
        """
        Method for logging a user with dummy data
        """
        return self.client.post(
            'api/v1/auth/login',
            data=json.dumps(
                dict(
                    email=email,
                    password=password
                )
            ),
            content_type='application/json'
        )

    def get_token(self):
        """
        Returns a user token
        """
        response = self.login_user("marie@live.com", "marie")
        data = json.loads(response.data.decode())
        return data['token']

    def add_meal(self, token, meal_name, price):
        """
        Function to create a meal
        """
        return self.client.post(
            'api/v1/meals',
            data=json.dumps(
                dict(
                    meal_name=meal_name,
                    price=price
                )
            ),
            content_type='application/json',
            headers=({"token": token})
        )

    def get_meals(self, token):
        """
        function to return meals
        """
        return self.client.get('api/v1/meals', headers=({"token": token}))
