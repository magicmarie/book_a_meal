
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api

import re
from . import meals

from app.api.models.meal import Meal
from .user_views import users_list, meals_list

api = Api(meals)


class MealsList(Resource):
    def get(self):
        items = []
        for user in users_list:
            admin = user.isAdmin
            if admin == "True":
                for meal in meals_list:
                    meals_data = {}
                    meals_data["id"] = meal.id,
                    meals_data["price"] = meal.price,
                    meals_data["meal_name"] = meal.meal_name
                    items.append(meals_data)
                return make_response(jsonify({"meals_items": items}), 200)
            return make_response(jsonify({"message": "Customer is not allowed to view this"}), 401)
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}), 401)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('meal_name', type=str, required=True)
        parser.add_argument('price', type=int, required=True)

        for user in users_list:
            admin = user.isAdmin
            if admin == "True":
                args = parser.parse_args()
                meal_name = args['meal_name']
                price = args['price']

                new_meal = Meal(meal_name, price)

                for meal in meals_list:
                    if meal_name == meal.meal_name:
                        return make_response(jsonify({"message": 'Meal name already exists'}), 400)
                meals_list.append(new_meal)
                return make_response(jsonify({
                    'message': 'Meal successfully created',
                    'status': 'success'},
                ), 201)
            return make_response(jsonify({"message": "Customer is not authorized to create meals"}), 401)
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}), 401)


api.add_resource(MealsList, '/api/v1/meals')


class MealOne(Resource):
    def get(self, meal_id):
        item = []
        for user in users_list:
            admin = user.isAdmin
            if admin == "True":
                for meal in meals_list:
                    if meal.id == meal_id:
                        meal_data = {}
                        meal_data["id"] = meal.id,
                        meal_data["price"] = meal.price,
                        meal_data["meal_name"] = meal.meal_name
                        item.append(meal_data)
                return make_response(jsonify({"meal_item": item[0]}), 200)
            return make_response(jsonify({"message": "Customer is not allowed to view this"}))
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}), 401)

    def put(self, meal_id):
        parser = reqparse.RequestParser()
        parser.add_argument('meal_name', type=str, required=True)
        parser.add_argument('price', type=int, required=True)

        for user in users_list:
            admin = user.isAdmin
            if admin == "True":
                for meal in meals_list:
                    if meal.id == meal_id:
                        args = parser.parse_args()
                        meal.meal_name = args['meal_name']
                        meal.price = args['price']
                        return make_response(jsonify({"message": "Meal updated successfully"}), 204)

    def delete(self, meal_id):
        for user in users_list:
            admin = user.isAdmin
            if admin == "True":
                for meal in meals_list:
                    if meal.id == meal_id:
                        meals_list.remove(meal)
                        return jsonify("Meal deleted succesfully")
            return make_response(jsonify({"message": "Customer is not allowed to do this"}))


api.add_resource(MealOne, '/api/v1/meals/<meal_id>')
