""" menu views"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from api.models.menu import Menu
from api.models.user import User
from api.models.meal import Meal
from api.auth_token import use_token
from . import menus

api = Api(menus)


class MenuPost(Resource):
    """menupost class"""
    @staticmethod
    @swag_from('../apidocs/add_menu.yml')
    def post(meal_id):
        """
        Allows authenticated admin to create a menu by adding a meal by Id from
        the meals table.
        token is required to get the admin Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)

        response = User.user_is_admin(res)
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 401)

        meal = Meal.find_meal(meal_id, res)
        if not meal['status']:
            return make_response(jsonify({
                "message": meal['message']
            }), 404)
        menu = Menu()
        new_menu = menu.save_menu(meal_id, res)
        if not new_menu['status']:
            return make_response(jsonify({
                "message": "Meal already exists in menu"
            }), 409)
        return make_response(jsonify({
            "message": "Meal successfully added to menu"
        }), 201)


api.add_resource(MenuPost, '/api/v1/menu/<int:meal_id>')


class Menus(Resource):
    """menu class"""
    @staticmethod
    @swag_from('../apidocs/get_menu.yml')
    def get():
        """
        Return the menu created by authenticated admin
        token is required to get the admin Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)

        menu = Menu.get_menu(res)
        if menu['status']:
            return make_response(jsonify({
                "Menu": menu['menu']
            }), 200)


api.add_resource(Menus, '/api/v1/menu')
