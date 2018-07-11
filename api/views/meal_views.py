""" meal views"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from api.models.meal import Meal
from api.auth_token import use_token
from api.models.user import User
from api import DB
from . import meals

api = Api(meals)


class Mealsdb(Resource):
    """mealsdb class"""
    @staticmethod
    @swag_from('../apidocs/add_meal.yml')
    def post():
        """
        Allows authenticated admin to create a meal
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            'meal_name',
            type=str,
            help="mneal_name is a required field",
            required=True)
        parser.add_argument(
            'price',
            help="Price is a required field",
            required=True)
        args = parser.parse_args()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)
        meal = Meal(meal_name=args["meal_name"], price=args['price'])
        response = User.user_is_admin(res)
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 401)
        validate = meal.validate_inputs()
        if not validate['status']:
            return make_response(jsonify({
                "message": validate['message']
            }), 400)
        new_meal = meal.save_meal(args["meal_name"], args['price'], res)
        if not new_meal['status']:
            return make_response(jsonify({
                "message": 'Meal name already exists'
            }), 409)
        return make_response(jsonify({
            'message': 'Meal successfully created'
        }), 201)

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

        response = User.user_is_admin(res)
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 401)
        meals = Meal.get_meals(res)
        meal_items = Meal.meals_serializer(meals)
        return make_response(jsonify({
            "meal_items": meal_items
        }), 200)


api.add_resource(Mealsdb, '/api/v1/meals')


class MealOne(Resource):
    """mealone class"""
    @staticmethod
    @swag_from('../apidocs/delete_meal.yml')
    def delete(meal_id):
        """
        Deletes a meal from the database if it exists
        token is required to get admin Id
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
        meal['meal'].delete_meal()
        return make_response(jsonify({
            "message": "Meal deleted succesfully"
        }), 200)

    @staticmethod
    @swag_from('../apidocs/edit_meal.yml')
    def put(meal_id):
        """
        Allows admin to edit the meal details from the meals_list if it exists.
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            'meal_name',
            type=str,
            help="meal_name is a required field",
            required=True)
        parser.add_argument(
            'price',
            help="Price is a required field",
            required=True)
        args = parser.parse_args()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)

        response = User.user_is_admin(res)
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 401)
        res1 = Meal.find_meal(meal_id, res)
        if not res1['status']:
            return make_response(jsonify({
                "message": res1['message']
            }), 404)
        new_meal = res1['meal'].edit_meal(args['meal_name'], args['price'])
        response = new_meal['meal'].validate_inputs()
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 400)
        DB.session.commit()
        return make_response(jsonify({
            "message": "Meal updated successfully"
        }), 201)


api.add_resource(MealOne, '/api/v1/meals/<int:meal_id>')
