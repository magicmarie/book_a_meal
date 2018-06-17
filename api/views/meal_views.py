""" meal views"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from api.models import User, Meal, validate_inputs, use_token
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
        parser.add_argument('meal_name', type=str, required=True)
        parser.add_argument('price', type=int, required=True)
        args = parser.parse_args()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 400)

        user = User.query.filter_by(id=res['decoded']['id'], is_admin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not authorized to create meals"
            }), 401)
        meal_name = args['meal_name']
        price = args['price']

        response = validate_inputs(meal_name)
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 400)

        meal = Meal.query.filter_by(meal_name=meal_name, userId=res['decoded']['id']).first()
        if meal:
            return make_response(jsonify({
                "message": 'Meal name already exists'
            }), 400)
        new_meal = Meal(meal_name=meal_name, price=price, userId=res['decoded']['id'])
        DB.session.add(new_meal)
        DB. session.commit()
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
            return make_response(jsonify({"message": res['message']}), 400)

        user = User.query.filter_by(id=res['decoded']['id'], is_admin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not authorized to view meals"
            }), 401)
        meals = Meal.query.filter_by(userId=res['decoded']['id']).all()
        meal_items = []
        for meal in meals:
            meal_data = {
                "id": meal.id,
                "price": meal.price,
                "meal_name": meal.meal_name,
                "userId": meal.userId
            }
            meal_items.append(meal_data)
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
            return make_response(jsonify({"message": res['message']}), 400)

        user = User.query.filter_by(id=res['decoded']['id'], is_admin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not allowed to do this"
            }), 401)

        meal = Meal.query.filter_by(userId=res['decoded']['id'], id=meal_id).first()
        if not meal:
            return make_response(jsonify({
                "message": "Meal not found"
            }), 404)
        DB.session.delete(meal)
        DB.session.commit()
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
        parser.add_argument('meal_name', type=str, required=True)
        parser.add_argument('price', type=int, required=True)
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 400)

        user = User.query.filter_by(id=res['decoded']['id'], is_admin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not allowed to do this"
            }), 401)

        meal = Meal.query.filter_by(userId=res['decoded']['id'], id=meal_id).first()
        if not meal:
            return make_response(jsonify({
                "message": "Meal not found"
            }), 404)
        args = parser.parse_args()
        response = validate_inputs(args['meal_name'])
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 400)
        meal.meal_name = args['meal_name']
        meal.price = args['price']
        DB.session.add(meal)
        DB.session.commit()
        return make_response(jsonify({
            "message": "Meal updated successfully"
        }), 201)


api.add_resource(MealOne, '/api/v1/meals/<int:meal_id>')
