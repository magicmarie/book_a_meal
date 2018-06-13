import os
import config
from flask import Flask
from flask_restful import Api, reqparse, Resource
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

# initialise app
APP = Flask(__name__)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SECRET_KEY'] = os.urandom(24)
APP.config.from_object(config.app_config['development'])

# create instance of app in api
API = Api(APP)

# instance of app in SQLAlchemy
DB = SQLAlchemy(APP)

from .models import *

APP.config['swagger'] = {'swagger': '2.0', 'title': 'Book-a-meal-api', \
            'description': "is a web based app that enables users to \
            checkout menus, make orders and also check their order \
            history. The meals, menus are made by the caterers, who \
               view the user orders as well.",
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
                                 'description': 'Meal options(create, read, \
                                 update, delete) for a caterer'
                             },
                             {
                                 'name': 'Menu',
                                 'description': 'Menu a meal option is added to'
                             },
                             {
                                 'name': 'Order',
                                 'description': 'Meal request made by \
                                  authenticated users'}]}

swagger = Swagger(APP)

from .views import *
# register blueprints
APP.register_blueprint(users)
APP.register_blueprint(meals)
APP.register_blueprint(menus)
APP.register_blueprint(orders)
