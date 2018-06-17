""" menu views"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from api.models import User, Menu, Meal, use_token
from api import DB
from . import menus

api = Api(menus)


class MenuPost(Resource):
    """menupost class"""
    @staticmethod
    @swag_from('../apidocs/add_menu.yml')
    def post(meal_id):
        """
        Allows authenticated admin to create a menu by adding a meal by Id from
        the meals table.
        token is required to get the admin Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 400)

        user = User.query.filter_by(id=res['decoded']['id'], is_admin="True").first()
        if not user:
            return make_response(jsonify({
                "message": "Customer is not allowed to do this"
            }), 401)

        meal = Meal.query.filter_by(
            id=meal_id, userId=res['decoded']['id']).first()
        if not meal:
            return make_response(jsonify({
                "message": "Meal not found"
            }), 404)

        mymeal = Menu.query.filter_by(mealId=meal_id).first()
        if not mymeal:
            menu = Menu(mealId=meal_id)
            DB.session.add(menu)
            DB.session.commit()
            return make_response(jsonify({
                "message": "Meal successfully added to menu"
            }), 200)

        if meal.userId == res['decoded']["id"]:
            return make_response(jsonify({
                "message": "Meal already exists in menu"
            }), 409)
        return make_response(jsonify({
            "message": "You are not authorized to perform that action"
        }), 404)


api.add_resource(MenuPost, '/api/v1/menu/<int:meal_id>')


class Menus(Resource):
    """menu class"""
    @staticmethod
    @swag_from('../apidocs/get_menu.yml')
    def get():
        """
        Return the menu created by authenticated admin
        token is required to get the admin Id
        """
        parser = reqparse.RequestParser()
        res = use_token(parser)
        if not res['status']:
            return make_response(jsonify({"message": res['message']}), 400)

        user = User.query.filter_by(id=res['decoded']['id']).first()
        if not user:
            return make_response(jsonify({
                "message": "Doesn't exist, Create an account"
            }))
        menu = Menu.query.all()
        menu_items = []
        if not menu:
            return make_response(jsonify({
                "message": "Menu name does not exist"
            }))
        for menu_item in menu:
            menu_data = {
                "meal_id": menu_item.meal.id,
                "meal_name": menu_item.meal.meal_name,
                "price": menu_item.meal.price
            }
            menu_items.append(menu_data)
        return make_response(jsonify({"menu": menu_items}), 200)


api.add_resource(Menus, '/api/v1/menu')
