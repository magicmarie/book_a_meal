"""views"""
from flask import Blueprint

users = Blueprint('users', __name__)
meals = Blueprint('meals', __name__)
menus = Blueprint('menus', __name__)
orders = Blueprint('orders', __name__)

from . import user_views, meal_views, menu_views, order_views
