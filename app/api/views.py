import json
import jwt
from datetime import datetime, timedelta
# third party imports
from flask import jsonify, make_response
from flask_restful import Resource, Api, reqparse, abort
import uuid

# local imports
from . import api

from .models.user import User
from .models.meal import Meal
from .models.menu import Menu
from .models.order import Order

users_list = []
meals_list = []
menu_list = []
order_list = []


class Signup(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('confirm_password', required=True)
        parser.add_argument('isAdmin', type=str, required=True)

        args = parser.parse_args()
        name = args['name']
        email = args['email']
        password = args['password']
        confirm_password = args['confirm_password']
        isAdmin = args['isAdmin']

        if password != confirm_password:
            return make_response(jsonify({"message": "passwords don't match"}), 401)

        new_user = User(name, email, password, confirm_password, isAdmin)

        for user in users_list:
            if email == user.email:
                return make_response(jsonify({"message": "email in use already"}), 400)
        users_list.append(new_user)
        return make_response(jsonify(new_user.__dict__), 201)


api.add_resource(Signup, '/api/v1/auth/signup')


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()
        email = args['email']
        password = args['password']

        for user in users_list:
            if email == user.email and password == user.password:
                admin = user.isAdmin
                if admin == "True":
                    access_token = user.generate_token(user.id)
                    print(access_token)
                    if access_token:
                        return make_response(jsonify({"message": "Logged in succesfully",
                                                      "email": user.email,
                                                      "id": user.id,
                                                      "Admin": user.isAdmin,
                                                      "access_token": access_token}), 200)
                return make_response(jsonify({"message": "Logged in succesfully",
                                              "email": user.email,
                                              "id": user.id,
                                              "Admin": user.isAdmin,
                                              }), 200)
            return make_response(jsonify("wrong credentials"), 401)


api.add_resource(Login, '/api/v1/auth/login')


class MealsList(Resource):
    def get(self):
        items = []
        for meal in meals_list:
            meals_data = {}
            meals_data["id"] = meal.id,
            meals_data["price"] = meal.price,
            meals_data["meal_name"] = meal.meal_name
            items.append(meals_data)
        return make_response(jsonify({"meals_items": items}), 200)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('meal_name', required=True)
        parser.add_argument('price', required=True)

        # for user in users_list:
        # admin = user.isAdmin
        # if admin == "True":
        args = parser.parse_args()
        meal_name = args['meal_name']
        price = args['price']

        new_meal = Meal(meal_name, price)

        for meal in meals_list:
            if meal_name == meal.meal_name:
                return jsonify("Meal  name exists already")
        meals_list.append(new_meal)
        return jsonify(new_meal.__dict__)
        # return jsonify("Not authorized to create meals")


api.add_resource(MealsList, '/api/v1/meals')


class Menus(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('menu_name', required=True)

        args = parser.parse_args()
        menu_name = args['menu_name']

        new_menu = Menu(menu_name)
        print(new_menu)
        for menu in menu_list:
            if menu_name == menu.menu_name:
                return make_response(jsonify("Menu name exists already"), 422)
        menu_list.append(new_menu)
        return make_response(jsonify({"message": "Menu successfully created",
                                      "menu": new_menu.__dict__}), 201)


api.add_resource(Menus, '/api/v1/menu')


class Orders(Resource):
    def get(self):
        #     return json.dumps(meals_list)
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('meal_name', required=True)
        parser.add_argument('price', required=True)

        args = parser.parse_args()
        meal_name = args['meal_name']
        price = args['price']

        new_order = Order(meal_name, price)

        order_list.append(new_order)
        return make_response(jsonify({"message": "Order succesfully sent", "order": new_order.__dict__}), 201)


api.add_resource(Orders, '/api/v1/order')
