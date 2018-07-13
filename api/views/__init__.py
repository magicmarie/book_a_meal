"""blueprints"""
from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint("api", __name__)

api = Api(api_bp)

from .user_views import Signup, Login
from .meal_views import Mealsdb, MealOne
from .menu_views import Menus, MenuPost
from .order_views import OrderGet, OrdersGet, OrderPost

api.add_resource(Signup, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(Mealsdb, '/meals')
api.add_resource(MealOne, '/meals/<int:meal_id>')
api.add_resource(MenuPost, '/menu/<int:meal_id>')
api.add_resource(Menus, '/menu')
api.add_resource(OrderPost, '/orders/<menu_id>/<meal_id>')
api.add_resource(OrdersGet, '/orders')
api.add_resource(OrderGet, '/user/orders')
