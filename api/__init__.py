from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, reqparse, Resource

# initialise app
APP = Flask(__name__)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config.from_object('config')

# create instance of app in api
API = Api(APP)

# instance of app in SQLAlchemy
DB = SQLAlchemy(APP)
DB.init_app(APP)
