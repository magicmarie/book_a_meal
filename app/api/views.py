from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import my_api as api
import re

from .models.user import User, generate_token
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
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('isAdmin', type=str, required=True)

        args = parser.parse_args()
        name = args['name']
        email = args['email']
        password = args['password']
        isAdmin = args['isAdmin']

        if name.strip() == "":
            return make_response(jsonify({"message": "invalid, Enter name please"}), 401)

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return make_response(jsonify({"message": "Enter valid email "}), 401)

        if password.strip() == "":
            return make_response(jsonify({"message": "Enter password"}), 401)

        if len(password) < 5:
            return make_response(jsonify({"message": "Password is too short, < 5"}), 401)

        new_user = User(name, email, password, isAdmin)

        for user in users_list:
            if email == user.email:
                return make_response(jsonify({"message": "email already in use"}), 400)

        users_list.append(new_user)
        return make_response(jsonify({'message': 'User successfully created'}), 201)


api.add_resource(Signup, '/api/v1/auth/signup')


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        args = parser.parse_args()
        email = args['email']
        password = args['password']

        for user in users_list:
            if email == user.email and password == user.password:
                access_token = "{}".format(generate_token(user.id))
                return make_response(jsonify({"token": access_token,
                                              "message": "User logged in successfully"
                                              }), 200)
        return make_response(jsonify({"message": "wrong credentials"}), 401)


api.add_resource(Login, '/api/v1/auth/login')


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


class Menus(Resource):
    def get(self, menu_id):
        item = []
        for user in users_list:
            for menu in menu_list:
                if menu.id == menu_id:
                    menu_data = {}
                    menu_data["id"] = menu.id
                    menu_data["menu__name"] = menu.menu_name
                    item.append(menu_data)
            return make_response(jsonify({"menu_item": item[0]}), 200)
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}))


api.add_resource(Menus, '/api/v1/menu')


class OrderOne(Resource):

    def delete(self, order_id):
        for user in users_list:
            admin = user.isAdmin
            if admin == "False":
                for meal in meals_list:
                    if meal.id == id:
                        order_list.remove(meal)
                        return make_ressponse(jsonify({"meassage": "Order deleted succesfully"}), 200)


api.add_resource(OrderOne, '/api/v1/orders/<order_id>')


class MenuPost(Resource):
    def post(self, meal_id):
        for user in users_list:
            admin = user.isAdmin
            if admin == "True":
                for meal in meals_list:
                    if meal_id == meal.id:
                        menu_list.append(meal)
                        return make_response(jsonify({"message": "Meal successfully added to menu",
                                                      "status": "success"}), 201)
                    return make_response(jsonify({"meassage": "Meal does not exist"}))
            return make_response(jsonify({"message": "Customer is not allowed to do this"}), 400)


api.add_resource(MenuPost, '/api/v1/menu/<meal_id>')


class OrderPost(Resource):
    def post(self, meal_id):
        for user in users_list:
            for meal in meals_list:
                if meal_id == meal.id:
                    order_list.append(meal)
                    return make_response(jsonify({"message": "Order sent successfully",
                                                  "status": "success"}), 201)
                return make_response(jsonify({"meassage": "Meal does not exist"}))


api.add_resource(OrderPost, '/api/v1/orders/<meal_id>')


class OrdersGet(Resource):
    def get(self):
        for user in users_list:
            admin = user.isAdmin
            if admin == "True":
                return make_response(jsonify({"Orders": order_list}), 200)
            return make_response(jsonify({"message": "Customer is not allowed to view this"}), 401)
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}), 401)


api.add_resource(OrdersGet, '/api/v1/orders')
