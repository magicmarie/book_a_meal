""" order views"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from
from api.models import User, Menu, Order, use_token
from api import DB
from . import orders

api = Api(orders)


class OrderPost(Resource):
    """orderpost class"""
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
            return make_response(jsonify({"message": res['message']}), 401)

        order = Menu.query.filter_by(mealId=meal_id).first()
        if not order:
            return make_response(jsonify({
                "message": "Meal does not exist"
            }), 404)
        new_order = Order(mealId=meal_id, \
        userId=res['decoded']['id'], adminId=order.meal.userId)
        DB.session.add(new_order)
        DB.session.commit()
        return make_response(jsonify({
            "message": "Order sent successfully"
        }), 201)


api.add_resource(OrderPost, '/api/v1/orders/<meal_id>')


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
        total = 0
        response = User.user_is_admin(res)
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 401)
        orderz = Order.query.filter_by(adminId=res['decoded']['id']).all()
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

        order = Order.query.filter_by(userId=res['decoded']['id']).all()
        user_order_items = []
        if not order:
            return make_response(jsonify({"message": "No orders found"}), 404)
        for item in order:
            user_order_data = {
                "id": item.id,
                "mealId": item.mealId,
                "userId": item.userId
            }
            user_order_items.append(user_order_data)
        return make_response(jsonify({
            "Orders": user_order_items,
            "status": "success"
        }), 200)


api.add_resource(OrderGet, '/api/v1/user/orders')
