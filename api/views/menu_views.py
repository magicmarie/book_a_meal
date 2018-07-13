""" menu views"""
from flask import jsonify, make_response, g
from flask_restful import Resource, reqparse, Api, abort
from flasgger.utils import swag_from
from .decorators import authenticate, admin_required
from api.models.menu import Menu
from api.models.user import User
from api.models.meal import Meal


class MenuPost(Resource):
    """menupost class"""
    @staticmethod
    @authenticate
    @admin_required
    @swag_from('../apidocs/add_menu.yml')
    def post(meal_id):
        """
        Allows authenticated admin to create a menu by adding a meal by Id from
        the meals table.
        token is required to get the admin Id
        """
        meal = Meal.find_meal(meal_id, g.user)
        if not meal['status']:
            abort(http_status_code=400, message=meal['message'])
        menu = Menu()
        new_menu = menu.save_menu(meal_id, g.user)
        if not new_menu['status']:
            abort(http_status_code=409, message="Meal already exists in menu")
        return make_response(jsonify({
            "message": "Meal successfully added to menu"
        }), 201)


class Menus(Resource):
    """menu class"""
    @staticmethod
    @authenticate
    @admin_required
    @swag_from('../apidocs/get_menu.yml')
    def get():
        """
        Return the menu created by authenticated admin
        token is required to get the admin Id
        """
        menu = Menu.get_menu(g.user)
        if menu['status']:
            return make_response(jsonify({
                "Menu": menu['menu']
            }), 200)
