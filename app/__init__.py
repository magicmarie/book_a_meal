# third-party imports
import os
from flask import Flask
from app.models import user
from config import app_config

# local imports
# import the user, business and review classes
user_object = user.User()


def create_app(config_name):
    # Initialize flask app
    app = Flask(__name__)
    # load from config.py in root folder
    app.config.from_object(app_config[config_name])
    app.config['SECRET_KEY'] = 'mariam'

    from .api import api as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
