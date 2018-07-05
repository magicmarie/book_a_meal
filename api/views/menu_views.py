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
            return make_response(jsonify({"message": res['message']}), 401)

        response = User.user_is_admin(res)
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 401)

        meal = Meal.find_meal(meal_id, res)
        if not meal['status']:
            return make_response(jsonify({
                "message": meal['message']
            }), 404)
        menu = Menu().save_menu(meal_id, res)
        if not menu['status']:
            return make_response(jsonify({
                "message": menu['message']
            }), 409)
        return make_response(jsonify({
                "message": menu['message']
            }), 201)

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
            return make_response(jsonify({"message": res['message']}), 401)

        menu = Menu.get_menu(res)
        if menu['status']:
           return make_response(jsonify({
                "message": menu['menu']
            }), 200) 
        # user = User.query.filter_by(id=res['decoded']['id']).first()
        # if user: 
        #     menu = Menu.query.all()
        #     menu_items = []
        #     if menu:
        #         for menu_item in menu:
        #             menu_data = {
        #                 "meal_id": menu_item.meal.id,
        #                 "meal_name": menu_item.meal.meal_name,
        #                 "price": menu_item.meal.price
        #             }
        #             menu_items.append(menu_data)
        #         return make_response(jsonify({"menu": menu_items}), 200)


api.add_resource(Menus, '/api/v1/menu')
