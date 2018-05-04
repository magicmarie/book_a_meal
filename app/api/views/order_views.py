from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api

import re
import json
from . import orders
from app.api.models.order import Order
from .user_views import users_list, meals_list, order_list

from app.api.models.user import decode_token

api = Api(orders)


class OrderOne(Resource):
    def put(self, order_id):
        parser = reqparse.RequestParser()
        parser.add_argument('meal_id', type=str, required=True)
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        for order in order_list:
            if order['id'] == order_id:
                if order["user_id"] == decoded["id"]:
                    order["meal_id"] = args['meal_id']
                    return make_response(jsonify({"message": "Order deleted succesfully"}), 200)
                return make_response(jsonify({"message": "You can not update that order"}), 401)
        return make_response(jsonify({"message": "Order not found"}), 400)


api.add_resource(OrderOne, '/api/v1/orders/<order_id>')


class OrderPost(Resource):
    def post(self, meal_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        new_order = Order(meal_id, decoded["id"])
        for meal in meals_list:
            if meal_id == meal["id"]:
                order_list.append(json.loads(new_order.json()))
                return make_response(jsonify({"message": "Order sent successfully",
                                              "status": "success"}), 201)
        return make_response(jsonify({"meassage": "Meal does not exist"}))


api.add_resource(OrderPost, '/api/v1/orders/<meal_id>')


class OrdersGet(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        for user in users_list:
            if user['id'] == decoded['id']:
                if decoded['isAdmin'] == "True":
                    return make_response(jsonify({"Orders": order_list, "message":"Order sent successfully"}), 200)
            return make_response(jsonify({"message": "Customer is not allowed to view this"}), 401)
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}), 401)


api.add_resource(OrdersGet, '/api/v1/orders')
