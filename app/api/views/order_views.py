from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api

import re
from . import orders
from app.api.models.order import Order
from .user_views import users_list, meals_list, order_list

api = Api(orders)


class OrderOne(Resource):

    def delete(self, order_id):
        for user in users_list:
            admin = user.isAdmin
            if admin == "False":
                for meal in meals_list:
                    if meal.id == id:
                        order_list.remove(meal)
                        return make_response(jsonify({"meassage": "Order deleted succesfully"}), 200)


api.add_resource(OrderOne, '/api/v1/orders/<order_id>')


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
