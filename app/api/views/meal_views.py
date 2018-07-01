""" meal views"""
import json
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from app.api.models.meal import Meal
from app.api.models.meal import meals_list
from app.api.models.user import use_token, users_list
from . import meals

api = Api(meals)

class MealsList(Resource):
    """ meal list class"""
    @staticmethod
    @swag_from('../apidocs/get_meals.yml')
    def get():
        """
        Return all meals created by authenticated admin
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)

        items = []
        if res['decoded']['is_admin'] == "False":
            return make_response(jsonify({
                "message": "Customer is not allowed to view this"
            }), 401)
        for meal in meals_list:
            if meal.admin_id == res['decoded']['id']:
                meals_data = {
                    "id": meal.id,
                    "price": meal.price,
                    "meal_name": meal.meal_name,
                    "admin_id": meal.admin_id
                }
                items.append(meals_data)
        return make_response(jsonify({"meals_items": items}), 200)

    @staticmethod
    @swag_from('../apidocs/add_meal.yml')
    def post():
        """
        Allows authenticated admin to create a meal
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('meal_name', type=str, help="Meal_name is required", required=True)
        parser.add_argument('price', type=int, help="Price is required", required=True)
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)
        args = parser.parse_args()
        for user in users_list:
            if user['id'] == res['decoded']['id'] and res['decoded']['is_admin'] == "True":
                meal = Meal(
                    args['meal_name'],
                    args['price'],
                    res['decoded']['id'])
                res = meal.validate_inputs()
                if not res['status']:  
                    return make_response(jsonify({
                        "message": res['message']
                    }), 400)
                response = meal.save()
                if not response['status']:
                    return make_response(jsonify({
                        "message": response['message']
                    }), 409)
                return make_response(jsonify({
                    "message": response['message']
                }), 201)
        return make_response(jsonify({
            'message':'Customer is not authorised to create meals'
        }), 401)

api.add_resource(MealsList, '/api/v1/meals')


class MealOne(Resource):
    """meal one class"""
    @staticmethod
    @swag_from('../apidocs/get_meal.yml')
    def get(meal_id):
        """
        Return a meal by Id created by authenticated admin
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)
        if res['decoded']['is_admin'] == "True":
            for meal in meals_list:
                if meal.id == meal_id and meal.admin_id == res['decoded']['id']:
                    meal_data = {
                        "id": meal.id,
                        "price": meal.price,
                        "meal_name": meal.meal_name,
                        "admin_id": meal.admin_id
                    }
                    return make_response(jsonify({
                        "meal_item": meal_data
                    }), 200)
            return make_response(jsonify({'message': 'Meal not found'}), 404)
        return make_response(jsonify({
            'message': 'Customer is not allowed to view this'
        }), 401)

    @staticmethod
    @swag_from('../apidocs/edit_meal.yml')
    def put(meal_id):
        """
        Allows admin to edit the meal details from
        the meals_list if it exists.
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('meal_name', type=str, help="meal_name is required", required=True)
        parser.add_argument('price', type=int, help="price is required", required=True)
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)
        args = parser.parse_args()
        if res['decoded']['is_admin'] == "True":
            for meal in meals_list:
                if meal.id == meal_id and meal.admin_id == res['decoded']['id']:
                    updated_meal = Meal(
                    args['meal_name'],
                    args['price'],
                    res['decoded']['id'])
                    response = updated_meal.validate_inputs()
                    if not response['status']:
                        return make_response(jsonify({
                            "message": response['message']
                        }), 400)
                    if meal.admin_id == res['decoded']['id']:
                        meal.meal_name = args['meal_name']
                        meal.price = args['price']
                        return make_response(jsonify({
                            "message": "Meal updated successfully"
                        }), 201)
            return make_response(jsonify({"message": "Meal not found"}), 404)
        return make_response(jsonify({
            "message": "Customer is not allowed to do this"
        }), 401)

    @staticmethod
    @swag_from('../apidocs/delete_meal.yml')
    def delete(meal_id):
        """
        Deletes a meal from the meals_list if it exists
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)
        for user in users_list:
            if user['id'] == res['decoded']['id'] and res['decoded']['is_admin'] == "True":
                response = Meal.delete_meal(meal_id)
                if not response['status']:
                    return make_response(jsonify({"message": response['message']}), 404)
                return make_response(jsonify({"message": response['message']}), 200)
        return make_response(jsonify({
            "message": "Customer is not allowed to do this"
        }))

api.add_resource(MealOne, '/api/v1/meals/<meal_id>')
