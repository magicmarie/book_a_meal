from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

import re
import json
from . import meals

from app.api.models.meal import Meal
from .user_views import users_list, meals_list
from app.api.models.user import decode_token

api = Api(meals)


class MealsList(Resource):
    def get(self):
        """
        Return all meals created by authenticated admin
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        items = []
        if decoded['isAdmin'] == "False":
            return make_response(jsonify({"message": "Customer is not allowed to view this"}), 401)
        for meal in meals_list:
            if meal['admin_id'] == decoded['id']:
                meals_data = {
                    "id": meal["id"],
                    "price": meal['price'],
                    "meal_name": meal['meal_name'],
                    "admin_id": meal['admin_id']
                }
                items.append(meals_data)
        return make_response(jsonify({"meals_items": items}), 200)

    @swag_from('../apidocs/add_meal.yml')
    def post(self):
        """
        Allows authenticated admin to create a meal
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('meal_name', type=str, required=True)
        parser.add_argument('price', type=int, required=True)
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        for user in users_list:
            if user['id'] == decoded['id']:
                if decoded['isAdmin'] == "True":
                    meal_name = args['meal_name']
                    price = args['price']
                    if meal_name.strip() == "" or len(meal_name.strip()) < 2:
                        return make_response(jsonify({"message": "invalid, Enter name please"}), 401)

                    if re.compile('[!@#$%^&*:;?><.0-9]').match(meal_name):
                        return make_response(jsonify({"message": "Invalid characters not allowed"}))

                    new_meal = Meal(meal_name, price)

                    for meal in meals_list:
                        if meal_name == meal['meal_name'] and meal['admin_id'] == decoded['id']:
                            return make_response(jsonify({"message": 'Meal name already exists'}), 400)
                    meal = json.loads(new_meal.json())
                    meal['admin_id'] = decoded['id']
                    meals_list.append(meal)
                    return make_response(jsonify({
                        'message': 'Meal successfully created',
                        'status': 'success'},
                    ), 201)
                return make_response(jsonify({"message": "Customer is not authorized to create meals"}), 401)
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}), 401)


api.add_resource(MealsList, '/api/v1/meals')


class MealOne(Resource):
    def get(self, meal_id):
        """
        Return a meal by Id created by authenticated admin
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        if decoded['isAdmin'] == "True":
            for meal in meals_list:
                if meal['id'] == meal_id and meal['admin_id'] == decoded['id']:
                    meal_data = {
                        "id": meal['id'],
                        "price": meal['price'],
                        "meal_name": meal['meal_name'],
                        "admin_id": meal['admin_id']
                    }
                    return make_response(jsonify({"meal_item": meal_data}), 200)
            return make_response(jsonify({"message": "Meal not found"}), 404)
        return make_response(jsonify({"message": "Customer is not allowed to view this"}), 401)

    def put(self, meal_id):
        """
        Allows admin to edit the meal details from the meals_list if it exists.
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('meal_name', type=str, required=True)
        parser.add_argument('price', type=int, required=True)
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        for user in users_list:
            if user['id'] == decoded['id']:
                if decoded['isAdmin'] == "True":
                    for meal in meals_list:
                        if meal['id'] == meal_id:
                            args = parser.parse_args()
                            meal['meal_name'] = args['meal_name']
                            meal['price'] = args['price']

                            return make_response(jsonify({"message": "Meal updated successfully",
                                                          "list": "meals_list"}), 201)
                    return make_response(jsonify({"message": "Meal not found"}), 200)
            return make_response(jsonify({"message": "Customer is not allowed to do this"}))

    def delete(self, meal_id):
        """
        Deletes a meal from the meals_list if it exists
        token is required to get admin Id
        """
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
                if decoded['isAdmin'] == "True":
                    print(meals_list)
                    print(meal_id)
                    for meal in meals_list:
                        if meal['id'] == meal_id:
                            meals_list.remove(meal)
                            return jsonify("Meal deleted succesfully")
                    return make_response(jsonify({"message": "Meal not found"}), 200)
                return make_response(jsonify({"message": "Customer is not allowed to do this"}))


api.add_resource(MealOne, '/api/v1/meals/<meal_id>')
