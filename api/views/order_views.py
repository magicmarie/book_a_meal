import re
import json
import jwt

from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from . import orders
from api.models import User, Menu, Meal, Order, decode_token
from api import DB

api = Api(orders)


class OrderPost(Resource):
    @swag_from('../apidocs/add_order.yml')
    def post(self, meal_id):
        """
        Allows authenticated user to make an order from the menu
        token is required to get user Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        order = Menu.query.filter_by(mealId=meal_id).first()
        if not order:
            return make_response(jsonify({
                "meassage": "Meal does not exist"
            }), 404)
        new_order = Order(mealId=meal_id, userId=decoded['id'], adminId=order.meal.userId)
        DB.session.add(new_order)
        DB.session.commit()
        return make_response(jsonify({
            "message": "Order sent successfully"
        }), 201)


api.add_resource(OrderPost, '/api/v1/orders/<meal_id>')


class OrdersGet(Resource):
    @swag_from('../apidocs/get_orders.yml')
    def get(self):
        """
        Returns all orders made for authenticated admin
        token is required to get admin id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)
        total = 0
        user = User.query.filter_by(id=decoded['id'], isAdmin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not allowed to view this"
            }), 401)
        orderz = Order.query.filter_by(adminId=decoded['id']).all()
        order_items = []
        for order in orderz:
            order_data = {
                "id": order.id,
                "mealId": order.mealId,
                "userId": order.userId
            }
            order_items.append(order_data)
            total += order.meal.price
        return make_response(jsonify({
            "order_items": order_items,
            "Total": total
        }), 200)


api.add_resource(OrdersGet, '/api/v1/orders')


class OrderGet(Resource):
    @swag_from('../apidocs/get_order.yml')
    def get(self, user_id):
        """
        Return all orders made by authenticated user
        token is required to get user Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}), 400)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}), 400)

        order = Order.query.filter_by(userId=decoded['id']).all()
        my_order_items = []
        if not order:
            return make_response(jsonify({"message": "No orders found"}), 404)
        for item in order:
            my_order_data = {
                "id": item.id,
                "mealId": item.mealId,
                "userId": item.userId
            }
            my_order_items.append(my_order_data)
        return make_response(jsonify({
            "Orders": my_order_items, 
            "status": "success"
        }), 200)


api.add_resource(OrderGet, '/api/v1/orders/<user_id>')
