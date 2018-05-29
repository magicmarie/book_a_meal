import re
import json
import jwt

from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api

from . import meals
from api.models import User, Meal, decode_token
from api import DB

api = Api(meals)


class MealsList(Resource):
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
            return make_response(jsonify({
                "message": "Token is missing"
            }), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({
                "message": decoded["message"]
            }), 400)
        user = User.query.filter_by(
            id=decoded['id'], isAdmin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not authorized to create meals"
            }), 401)
        meal_name = args['meal_name']
        price = args['price']
        if meal_name.strip() == "" or len(meal_name.strip()) < 2:
            return make_response(jsonify({
                "message": "invalid, Enter meal name please"
            }), 400)
        if re.compile('[!@#$%^&*:;?><.0-9]').match(meal_name):
            return make_response(jsonify({
                "message": "Invalid characters not allowed"
            }), 401)

        meal = Meal.query.filter_by(meal_name=meal_name).first()
        if meal:
            return make_response(jsonify({
                "message": 'Meal name already exists'
            }), 400)
        new_meal = Meal(meal_name=meal_name, price=price, userId=decoded['id'])
        DB.session.add(new_meal)
        DB. session.commit()
        return make_response(jsonify({
            'message': 'Meal successfully created'
        }), 201)


api.add_resource(MealsList, '/api/v1/meals')
