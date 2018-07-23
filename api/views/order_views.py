""" order views"""
from flask import jsonify, make_response, g
from flask_restful import Resource
from flasgger.utils import swag_from

from .decorators import authenticate, admin_required
from api.models.order import Order

orderz = Order()


class OrderPost(Resource):
    """orderpost class"""
    @staticmethod
    @authenticate
    @swag_from('../apidocs/add_order.yml')
    def post(menu_id, meal_id):
        """
        Allows authenticated user to make an order from the menu
        token is required to get user Id
        """
        order = orderz.add_order(g.user, menu_id, meal_id)
        if not order['status']:
            return make_response(jsonify({
                "message": "Meal does not exist"
            }), 400)
        return make_response(jsonify({
            "message": "Order sent successfully"
        }), 201)


class OrdersGet(Resource):
    """ordersget class"""
    @staticmethod
    @authenticate
    @admin_required
    @swag_from('../apidocs/get_orders.yml')
    def get():
        """
        Returns all orders made for authenticated admin
        token is required to get admin id
        """
        res1 = orderz.get_admin_orders(g.user)
        return make_response(jsonify({
            "order_items": res1['order_items'],
            "Total": res1['total'],
            "status": res1['status']
        }), 200)


class OrderGet(Resource):
    """orderget class"""
    @staticmethod
    @authenticate
    @swag_from('../apidocs/get_order.yml')
    def get():
        """
        Return all orders made by authenticated user
        token is required to get user Id
        """
        response = Order().get_user_orders(g.user)
        return make_response(jsonify({
            "Orders": response['order_items']
        }), 200)
