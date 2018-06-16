""" menu views"""

from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from app.api.models.user import use_token
from .user_views import users_list, meals_list, menu_list
from . import menus

api = Api(menus)


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
        parser.add_argument('token', location='headers')
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 400)

        for user in users_list:
            if user['id'] == res['decoded']['id']:
                return make_response(jsonify({"menu": menu_list}), 200)
        return make_response(jsonify({
            "message": "Doesn't exist, Create an account please"
        }))


api.add_resource(Menus, '/api/v1/menu')


class MenuPost(Resource):
    """class menuspost"""
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
            return make_response(jsonify({"message": res['message']}), 400)

        if res['decoded']['is_admin'] == "True":
            for meal in menu_list:
                if meal_id == meal['id']:
                    if meal['admin_id'] == res['decoded']['id']:
                        return make_response(jsonify({
                            "message": "Meal already exists in menu"
                        }), 409)

            for meal in meals_list:
                if meal_id == meal['id']:
                    if meal['admin_id'] == res['decoded']['id']:
                        menu_list.append(meal)
                        return make_response(jsonify({
                            "message": "Meal successfully added to menu",
                            "status": "success"
                        }), 200)
                    return make_response(jsonify({
                        "message": "You are not allowed to add this meal to menu"
                    }), 401)
            return make_response(jsonify({
                "message": "Meal does not exist"
            }), 404)
        return make_response(jsonify({
            "message": "Customer is not allowed to do this"
        }), 400)


api.add_resource(MenuPost, '/api/v1/menu/<meal_id>')
