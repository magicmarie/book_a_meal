import re
import json
import jwt

from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api

from . import meals
from api.models import User, Meal, decode_token
from api import DB

api = Api(meals)


class Mealsdb(Resource):
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
        user = User.query.filter_by(id=decoded['id'], isAdmin="True").first()
        print(user)
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

        meal = Meal.query.filter_by(meal_name=meal_name, userId=decoded['id']).first()
        print(meal)
        if meal:
            return make_response(jsonify({
                "message": 'Meal name already exists'
            }), 400)
        else:
            new_meal = Meal(meal_name=meal_name, price=price, userId=decoded['id'])
            DB.session.add(new_meal)
            DB. session.commit()
            return make_response(jsonify({
                'message': 'Meal successfully created'
            }), 201)

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

        user = User.query.filter_by(id=decoded['id'], isAdmin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not authorized to view meals"
            }), 401)
        meals = Meal.query.filter_by(userId=decoded['id']).all()
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
    def delete(self, meal_id):
        """
        Deletes a meal from the database if it exists
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

        user = User.query.filter_by(id=decoded['id'],  isAdmin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not allowed to do this"
            }), 401)

        meal = Meal.query.filter_by(userId=decoded['id'], id=meal_id).first()
        if not meal:
            return make_response(jsonify({
                "message": "Meal not found"
            }), 404)
        DB.session.delete(meal)
        DB.session.commit()
        return make_response(jsonify({"message": "Meal deleted succesfully"}), 200)

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

        user = User.query.filter_by(id=decoded['id'], isAdmin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not allowed to do this"
            }), 401)

        meal = Meal.query.filter_by(userId=decoded['id'], id=meal_id).first()
        if not meal:
            return make_response(jsonify({
                "message": "Meal not found"
            }), 404)
        args = parser.parse_args()
        meal.meal_name = args['meal_name']
        meal.price = args['price']
        if args['meal_name'].strip() == "" or len(args['meal_name'].strip()) <2:
            return make_response(jsonify({
                "message": "invalid, Enter meal name please"
            }), 400)
        if re.compile('[!@#$%^&*:;?><.0-9]').match(args['meal_name']):
            return make_response(jsonify({
                "message": "Invalid characters not allowed"
            }), 401)
        DB.session.add(meal)
        DB.session.commit()
        return make_response(jsonify({
            "message": "Meal updated successfully"
        }), 201)


api.add_resource(MealOne, '/api/v1/meals/<int:meal_id>')
