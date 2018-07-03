"""menu views"""
import json
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from app.api.models.user import use_token, users_list
from app.api.models.meal import meals_list
from . import menus

api = Api(menus)
menu_list = []


class Menus(Resource):
    """class menus"""
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

        for user in users_list:
            if user['id'] == res['decoded']['id']:
                return make_response(jsonify({'menu': menu_list}), 200)

api.add_resource(Menus, '/api/v1/menu')


class MenuPost(Resource):
    """class menus post"""
    @staticmethod
    @swag_from('../apidocs/add_menu.yml')
    def post(meal_id):
        """
        Allows authenticated admin to create a menu by adding a meal
        by Id from the meals_list token is required to get the admin Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)

        if res['decoded']['is_admin'] == "True":
            for meal in menu_list:
                if meal_id == meal.id:
                    if meal.admin_id == res['decoded']['id']:
                        return make_response(jsonify({
                            "message": "Meal already exists in menu"
                        }), 409)

            for meal in meals_list:
                if meal_id == meal.id:
                    if meal.admin_id == res['decoded']['id']:
                        menu_list.append(json.loads(meal.json()))
                        return make_response(jsonify({
                            "message": "Meal successfully added to menu",
                        }), 200)
                    return make_response(jsonify({
                        "message": "You are not allowed to add this meal to menu"
                    }), 401)
            return make_response(jsonify({
                "message": "Meal does not exist"
            }), 404)

api.add_resource(MenuPost, '/api/v1/menu/<meal_id>')
