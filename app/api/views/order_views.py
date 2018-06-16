""" order views"""
import json
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from app.api.models.order import Order
from .user_views import order_list, menu_list, meals_list

from app.api.models.user import use_token
from . import orders

api = Api(orders)


class OrderOne(Resource):
    """class order one"""
    @staticmethod
    @swag_from('../apidocs/edit_order.yml')
    def put(order_id):
        """
        Returns an order made by authenticated user
        token is required to get user Id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('meal_id', type=str, required=True)
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 400)
        args = parser.parse_args()
        for order in order_list:
            if order['id'] == order_id:
                if order["user_id"] == res['decoded']["id"]:
                    order["meal_id"] = args['meal_id']
                    return make_response(jsonify({
                        "message": "Order updated succesfully"
                    }), 200)
                return make_response(jsonify({
                    "message": "You can not update that order"
                }), 401)
        return make_response(jsonify({"message": "Order not found"}), 404)


api.add_resource(OrderOne, '/api/v1/orders')


class OrderPost(Resource):
    """class orderpost"""
    @staticmethod
    @swag_from('../apidocs/add_order.yml')
    def post(meal_id):
        """
        Allows authenticated user to make an order from the menu
        token is required to get user Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 400)

        new_order = Order(meal_id, res['decoded']["id"])
        for meal in menu_list:
            if meal_id == meal["id"]:
                order_list.append({
                    "IDs": json.loads(new_order.json()),
                    "meal_name": meal['meal_name']
                })
                return make_response(jsonify({
                    "message": "Order sent successfully"
                }), 201)
        return make_response(jsonify({"meassage": "Meal does not exist"}), 404)


api.add_resource(OrderPost, '/api/v1/orders/<meal_id>')


class OrdersGet(Resource):
    """class ordersget"""
    @staticmethod
    @swag_from('../apidocs/get_orders.yml')
    def get():
        """
        Returns all orders made for authenticated admin
        token is required to get admin id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 400)
        my_orders = []
        total = 0
        if res['decoded']['is_admin'] == "True":
            for order in order_list:
                for meal in meals_list:
                    if order['IDs']['meal_id'] == meal['id']:
                        if meal['admin_id'] == res['decoded']['id']:
                            my_orders.append(order)
                            total += meal['price']
            if my_orders:
                return make_response(jsonify({"Orders": my_orders,
                                              "Total": total,
                                              "status": "success"
                                             }), 200)
            return make_response(jsonify({"message": "No orders found"}), 404)
        return make_response(jsonify({
            "message": "Customer is not allowed to view this"
        }), 401)


api.add_resource(OrdersGet, '/api/v1/orders')


class OrderGet(Resource):
    """class orderget"""
    @staticmethod
    @swag_from('../apidocs/get_order.yml')
    def get():
        """
        Return all orders made by authenticated user
        token is required to get user Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 400)

        ma_orders = []
        for order in order_list:
            if order['IDs']['user_id'] == res['decoded']['id']:
                ma_orders.append(order)

        if ma_orders:
            return make_response(jsonify({
                "Orders": ma_orders,
                "status": "success"
            }), 200)
        return make_response(jsonify({"message": "No orders found"}), 404)


api.add_resource(OrderGet, '/api/v1/user/orders')
