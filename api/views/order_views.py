""" order views"""
from flask import jsonify, make_response, g, request
from flask_restful import Resource
from flasgger.utils import swag_from
from api import DB
from .decorators import authenticate, admin_required
from api.models.order import Order

orderz = Order()


class OrderPost(Resource):
    """orderpost class"""
    @staticmethod
    @authenticate
    @swag_from('../apidocs/add_order.yml')
    def post(menu_id, meal_id, quantity):
        """
        Allows authenticated user to make an order from the menu
        token is required to get user Id
        """
        order = orderz.add_order(g.user, menu_id, meal_id, quantity)
        if not order['status']:
            return make_response(jsonify({
                "message": "Meal does not exist"
            }), 400)
        return make_response(jsonify({
            "message": "Order sent successfully",
            "order": order['order']
        }), 201)


class OrderDelete(Resource):
    """order delete class"""
    @staticmethod
    @authenticate
    def delete(order_id):
        """
        Allows authenticated user to delete an order made.
        token is required to get user Id
        """
        order = orderz.find_order(order_id, g.user)
        if not order['status']:
            return make_response(jsonify({
                "message": "Order does not exist"
            }), 400)
        DB.session.delete(order['order'])
        DB.session.commit()
        return make_response(jsonify({
            "message": "Order deleted successfully"
        }), 200)


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
        limit = request.args.get('limit', 10)
        page = request.args.get('page', 1)
        res1 = orderz.get_admin_orders(g.user, limit, page)
        return make_response(jsonify({
            "order_items": res1,
            "status": res1['status']
        }), 200)

    @authenticate
    def post(self):
        meals = request.json.get("meals", None)
        print(len(meals))
        for meal in meals:
            order = Order()
            ord = order.add_order(
                g.user, meal['menu_id'],
                meal['meal_id'],
                meal['quantity'])
        return make_response(jsonify({"message": "success"}))


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
        limit = request.args.get('limit', 12)
        page = request.args.get('page', 1)
        response = Order().get_user_orders(g.user, limit, page)
        return make_response(jsonify({
            "Orders": response
        }), 200)
