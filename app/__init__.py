"""app"""
from flask import Flask
from flasgger import Swagger
from .config import app_config


def create_app():
    """flask app instance"""
    # Initialize flask app
    app_ = Flask(__name__, instance_relative_config=True)

    return app_


app = create_app()
# load from config.py in root folder
app.config.from_object(app_config["development"])

app.config['swagger'] = {'swagger': '2.0', 'title': 'Book-a-meal-api', \
                         'description': "is a web based app that enables \
                         users to checkout menus, make orders and also \
                         check their order history. The meals, menus are \
                          made by the caterers, who view the user orders",
                         'basePath': '', 'version': '0.0.1', 'contact': {
                             'Developer': 'Mariam Natukunda',
                             'email': 'natukunda162@gmail.com'
                         }, 'license': {
                         }, 'tags': [
                             {
                                 'name': 'User',
                                 'description': 'The api user'
                             },
                             {
                                 'name': 'Meal',
                                 'description': 'Meal options(create, \
                                 read, update, delete) for a caterer'
                             },
                             {
                                 'name': 'Menu',
                                 'description': 'Menu a meal is added to'
                             },
                             {
                                 'name': 'Order',
                                 'description': 'Meal request made by \
                                  authenticated users'}]}

swagger = Swagger(app)

from .api.views import users, meals, menus, orders
app.register_blueprint(users)
app.register_blueprint(meals)
app.register_blueprint(menus)
app.register_blueprint(orders)
