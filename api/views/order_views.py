""" order views"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from api.models.user import User
from api.models.order import Order
from api.auth_token import use_token
from . import orders

api = Api(orders)
orderz = Order()

class OrderPost(Resource):
    """orderpost class"""
    @staticmethod
    @swag_from('../apidocs/add_order.yml')
    def post(menu_id, meal_id):
        """
        Allows authenticated user to make an order from the menu
        token is required to get user Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 401)
        order = orderz.add_order(res, menu_id, meal_id)
        if not order['status']:
            return make_response(jsonify({
                "message": "Meal does not exist"
            }), 404)
        return make_response(jsonify({
            "message": "Order sent successfully"
        }), 201)


api.add_resource(OrderPost, '/api/v1/orders/<menu_id>/<meal_id>')


class OrdersGet(Resource):
    """ordersget class"""
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
            return make_response(jsonify({"message": res['message']}), 401)

        response = User.user_is_admin(res)
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 401)
        res1 = orderz.get_admin_orders(res)
        if res1:
            return make_response(jsonify({
                "order_items": res1['order_items'],
                "Total": res1['total']
            }), 200)
        return make_response(jsonify({
            "message": "orders not found"
        }), 404)


api.add_resource(OrdersGet, '/api/v1/orders')


class OrderGet(Resource):
    """orderget class"""
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
            return make_response(jsonify({"message": res['message']}), 401)

        response = Order().get_user_orders(res)
        if not response['status']:
            return make_response(jsonify({
                "message": "No orders found"
            }), 404)
        return make_response(jsonify({
            "Orders": response['order_items']
        }), 200)


api.add_resource(OrderGet, '/api/v1/user/orders')
