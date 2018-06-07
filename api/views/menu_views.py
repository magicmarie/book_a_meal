import re
import json
import jwt

from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api

from . import menus
from api.models import User, Menu, Meal, decode_token
from api import DB

api = Api(menus)


class MenuPost(Resource):
    def post(self, meal_id):
        """
        Allows authenticated admin to create a menu by adding a meal by Id from
        the meals table.
        token is required to get the admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        user = User.query.filter_by(id=decoded['id'], isAdmin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not allowed to do this"
            }), 401)

        meal = Meal.query.filter_by(
            id=meal_id, userId=decoded['id']).first()
        if not meal:
            return make_response(jsonify({
                "message": "Meal not found"
            }), 404)

        mymeal = Menu.query.filter_by(mealId=meal_id).first()
        if not mymeal:
            menu = Menu(mealId=meal_id)
            DB.session.add(menu)
            DB.session.commit()
            return make_response(jsonify({
                "message": "Meal successfully added to menu"
            }), 200)

        if meal.userId == decoded["id"]:
            return make_response(jsonify({
                "message": "Meal already exists in menu"
            }), 409)
        else:
            return make_response(jsonify({
                "message": "You are not authorized to perform that action"
            }), 404)


api.add_resource(MenuPost, '/api/v1/menu/<int:meal_id>')


class Menus(Resource):
    def get(self):
        """
        Return the menu created by authenticated admin
        token is required to get the admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        user = User.query.filter_by(id=decoded['id']).first()
        if not user:
            return make_response(jsonify({
                "message": "Doesn't exist, Create an account"
            }))
        menu = Menu.query.all()
        menu_items = []
        for menu_item in menu:
            menu_data = {
                "id": menu_item.id,
                "price": menu_item.meal.price,
                "meal_name": menu_item.meal.meal_name,
                "AdminId": menu_item.meal.userId
            }
            menu_items.append(menu_data)
        return make_response(jsonify({"menu": menu_items}), 200)


api.add_resource(Menus, '/api/v1/menu')
