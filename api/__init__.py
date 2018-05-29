import os
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, reqparse, Resource

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
with APP.app_context():
    DB.create_all()

from .views import *
# register blueprints
APP.register_blueprint(users)
APP.register_blueprint(meals)
APP.register_blueprint(menus)
APP.register_blueprint(orders)
