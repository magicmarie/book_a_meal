from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api

import re
from . import menus
from app.api.models.menu import Menu
from .user_views import users_list, meals_list, menu_list
from app.api.models.user import decode_token


api = Api(menus)


class Menus(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        for user in users_list:
            if user['id'] == decoded['id']:
                return make_response(jsonify({"menu": menu_list}), 200)
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}))


api.add_resource(Menus, '/api/v1/menu')


class MenuPost(Resource):
    def post(self, meal_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        if decoded['isAdmin'] == "True":
            for meal in menu_list:
                if meal_id == meal['id'] and meal['admin_id'] == decoded['id']:
                    return make_response(jsonify({"message": "Meal already exists in menu"}), 409)
                return make_response(jsonify({"message": "You are not allowed to add this meal to menu"}), 409)

            for meal in meals_list:
                if meal_id == meal['id'] and meal['admin_id'] == decoded['id']:
                    menu_list.append(meal)
                    return make_response(jsonify({"message": "Meal successfully added to menu",
                                                  "status": "success"}), 200)
                return make_response(jsonify({"message": "You are not allowed to add this meal to menu"}))
            return make_response(jsonify({"message": "Meal does not exist"}))
        return make_response(jsonify({"message": "Customer is not allowed to do this"}), 400)


api.add_resource(MenuPost, '/api/v1/menu/<meal_id>')
