""" meal views"""
from flask import jsonify, make_response, g
from flask_restful import Resource, reqparse, abort
from flasgger.utils import swag_from
from .decorators import authenticate, admin_required
from api.models.meal import Meal
from api.models.user import User
from api import DB
from . import api


class Mealsdb(Resource):
    """mealsdb class"""
    @staticmethod
    @authenticate
    @admin_required
    @swag_from('../apidocs/add_meal.yml')
    def post():
        """
        Allows authenticated admin to create a meal
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            'meal_name', type=str,
            help="meal_name is a required field",
            required=True)
        parser.add_argument(
            'price', help="Price is a required field", required=True)
        args = parser.parse_args()

        meal = Meal(meal_name=args["meal_name"], price=args['price'])
        validate = meal.validate_inputs()
        if not validate['status']:
            abort(http_status_code=400, message=validate['message'])
        new_meal = meal.save_meal(args["meal_name"], args['price'], g.user)
        if not new_meal['status']:
            abort(http_status_code=409, message='Meal name already exists')
        return make_response(jsonify({
            'message': 'Meal successfully created'
        }), 201)

    @staticmethod
    @authenticate
    @admin_required
    @swag_from('../apidocs/get_meals.yml')
    def get():
        """
        Return all meals created by authenticated admin
        token is required to get admin Id
        """
        current_user = g.user
        meals = Meal.get_meals(current_user)
        meal_items = Meal.meals_serializer(meals)
        return make_response(jsonify({
            "meal_items": meal_items
        }), 200)


class MealOne(Resource):
    """mealone class"""
    @staticmethod
    @authenticate
    @admin_required
    @swag_from('../apidocs/delete_meal.yml')
    def delete(meal_id):
        """
        Deletes a meal from the database if it exists
        token is required to get admin Id
        """
        current_user = g.user

        meal = Meal.find_meal(meal_id, current_user)
        if not meal['status']:
            abort(http_status_code=400, message=meal['message'])
        meal['meal'].delete_meal()
        return make_response(jsonify({
            "message": "Meal deleted succesfully"
        }), 200)

    @staticmethod
    @authenticate
    @admin_required
    @swag_from('../apidocs/edit_meal.yml')
    def put(meal_id):
        """
        Allows admin to edit the meal details from the meals_list if it exists.
        token is required to get admin Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            'meal_name', type=str, help="meal_name is a required field",
            required=True)
        parser.add_argument(
            'price', help="Price is a required field", required=True)
        args = parser.parse_args()

        res1 = Meal.find_meal(meal_id, g.user)
        if not res1['status']:
            abort(http_status_code=400, message=res1['message'])
        new_meal = res1['meal'].edit_meal(args['meal_name'], args['price'])
        response = new_meal['meal'].validate_inputs()
        if not response['status']:
            abort(http_status_code=400, message=response['message'])
        DB.session.commit()
        return make_response(jsonify({
            "message": "Meal updated successfully"
        }), 201)
