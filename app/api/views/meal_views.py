from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api

import re
import json
from . import meals

from app.api.models.meal import Meal
from .user_views import users_list, meals_list
from app.api.models.user import decode_token

api = Api(meals)


class MealsList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        items = []
        for user in users_list:
            if user['id'] == decoded['id']:
                if decoded['isAdmin'] == "True":
                    for meal in meals_list:

                        meals_data = {
                            "id": meal["id"],
                            "price": meal['price'],
                            "meal_name": meal['meal_name']
                        }
                        items.append(meals_data)
                    return make_response(jsonify({"meals_items": items}), 200)
            return make_response(jsonify({"message": "Customer is not allowed to view this"}), 401)
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}), 400)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('meal_name', type=str, required=True)
        parser.add_argument('price', type=int, required=True)
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        # print(decoded)
        for user in users_list:
            # print(user)
            if user['id'] == decoded['id']:
                if decoded['isAdmin'] == "True":
                    meal_name = args['meal_name']
                    price = args['price']
                    if meal_name.strip() == "" or len(meal_name.strip()) < 2:
                        return make_response(jsonify({"message": "invalid, Enter name please"}), 401)

                    if re.compile('[!@#$%^&*:;?><.]').match(meal_name):
                        return make_response(jsonify({"message": "Invalid characters not allowed"}))

                    new_meal = Meal(meal_name, price)

                    for meal in meals_list:
                        if meal_name == meal['meal_name']:
                            return make_response(jsonify({"message": 'Meal name already exists'}), 400)
                    meals_list.append(json.loads(new_meal.json()))
                    return make_response(jsonify({
                        'message': 'Meal successfully created',
                        'status': 'success'},
                    ), 201)
                return make_response(jsonify({"message": "Customer is not authorized to create meals"}), 401)
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}), 401)


api.add_resource(MealsList, '/api/v1/meals')


class MealOne(Resource):
    def get(self, meal_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])

        for user in users_list:
            if user['id'] == decoded['id']:
                if decoded['isAdmin'] == "True":
                    for meal in meals_list:
                        if meal['id'] == meal_id:
                            meal_data = {
                                "id": meal['id'],
                                "price": meal['price'],
                                "meal_name": meal['meal_name']
                            }
                            return make_response(jsonify({"meal_item": meal_data}), 200)
                    return make_response(jsonify({"message": "Meal not found"}), 200)
                return make_response(jsonify({"message": "Customer is not allowed to view this"}))
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}), 401)

    def put(self, meal_id):
        parser = reqparse.RequestParser()
        parser.add_argument('meal_name', type=str, required=True)
        parser.add_argument('price', type=int, required=True)
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])

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
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
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
