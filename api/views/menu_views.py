""" menu views"""
from flask import jsonify, make_response, g
from flask_restful import Resource, abort
from flasgger.utils import swag_from
from .decorators import authenticate, admin_required
from api import DB
from api.models.menu import Menu
from api.models.meal import Meal
from api.models.user import User

DAYS = {
    'monday': 'monday',
    'tuesday': 'tuesday',
    'wednesday': 'wednesday',
    'thursday': 'thursday',
    'friday': 'friday',
    'saturday': 'saturday',
    'sunday': 'sunday'
}


class MenuPost(Resource):
    """menupost class"""
    @staticmethod
    @authenticate
    @admin_required
    @swag_from('../apidocs/add_menu.yml')
    def post(menu_day, meal_id):
        """
        Allows authenticated admin to create a menu of the day by adding a
        meal by Id from the meals table.
        token is required to get the admin Id
        """
        meal = Meal.find_meal(meal_id, g.user)
        if not meal['status']:
            abort(http_status_code=400, message=meal['message'])
        day = DAYS.get(menu_day.lower(), None)
        if day is None:
            abort(http_status_code=400, message="Menu does not exist")
        menu = Menu(menu_name=day)
        res = menu.save_menu(meal_id, g.user)
        if not res['status']:
            abort(http_status_code=409, message="Meal already exists in menu")
        return make_response(jsonify({
            "message": "Meal successfully added to menu"
        }), 201)


class MenuDelete(Resource):
    @staticmethod
    @authenticate
    @admin_required
    def delete(menu_id):
        """
        Allows authenticated admin to delete a meal from the menu
        token is required to get the admin Id
        """
        menu = Menu()
        meal = menu.find_menu_meal(menu_id, g.user)
        if not meal['status']:
            abort(http_status_code=400, message="Meal does not exist in menu")
        DB.session.delete(meal['meal'])
        DB.session.commit()
        return make_response(jsonify({
            "message": "Meal deleted succesfully"
        }), 200)


class Menus(Resource):
    """menu class"""
    @staticmethod
    @authenticate
    @swag_from('../apidocs/get_menu.yml')
    def get(menu_day):
        """
        Return the menu created by authenticated admins.
        token is required to get the user Id
        """
        users = User.query.filter_by(is_admin="True").all()
        user_menus = []
        for user in users:
            menus = Menu.query.filter_by(
                admin_id=user.id).filter_by(menu_name=menu_day.lower()).all()
            meals = []
            for menu in menus:
                meal = Meal.query.get(menu.meal_id)
                meals.append({
                    "menu_id": menu.id,
                    "id": meal.id,
                    "name": meal.meal_name,
                    "price": meal.price
                })
            user_menus.append({
                'userName': user.name,
                'meals': meals,
                'id': user.id
            })
        return make_response(jsonify({'menus': user_menus}))


class AdminMenus(Resource):
    """menu class"""
    @staticmethod
    @authenticate
    @admin_required
    @swag_from('../apidocs/get_menu.yml')
    def get():
        """
        Return the menu created by authenticated admins.
        token is required to get the admin Id
        """
        user = g.user
        q = Menu.query.filter_by(admin_id=user['id'])
        day_menus = []
        for day in DAYS:
            meals = []
            menus = q.filter_by(menu_name=day).all()
            for menu in menus:
                meal = Meal.query.get(menu.meal_id)
                meals.append({"id": menu.id,
                              "meal_id": meal.id,
                              "meal_name": meal.meal_name,
                              "price": meal.price
                              })
            day_menus.append({
                "name": day.capitalize(),
                "meals": meals
            })
        return make_response(jsonify({'menus': day_menus}))
