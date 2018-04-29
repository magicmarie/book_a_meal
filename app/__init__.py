# third-party imports
import os
from flask import Flask
from .config import app_config


def create_app(config_name):
    # Initialize flask app
    app = Flask(__name__)
    # load from config.py in root folder
    app.config.from_object(app_config[config_name])

    return app
