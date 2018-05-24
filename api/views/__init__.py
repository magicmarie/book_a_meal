from flask import Blueprint
from api import APP

users = Blueprint('users', __name__)
meals = Blueprint('meals', __name__)
menus = Blueprint('menus', __name__)
orders = Blueprint('orders', __name__)

from . import user_views, meal_views, menu_views, order_views
APP.register_blueprint(users)
APP.register_blueprint(meals)
APP.register_blueprint(menus)
APP.register_blueprint(orders)
