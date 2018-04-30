# third-party imports
import os
from flask import Flask
from flask_restful import Resource, Api
from .config import app_config


def create_app(config_name):
    # Initialize flask app
    app = Flask(__name__, instance_relative_config=True)

    return app


app = create_app("testing")
# load from config.py in root folder
app.config.from_object(app_config["testing"])


my_api = Api(app)
from .api import views
