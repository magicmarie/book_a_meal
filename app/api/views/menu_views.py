from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api

import re
from . import menus
from app.api.models.menu import Menu
from .user_views import users_list, meals_list, menu_list

api = Api(menus)


class Menus(Resource):
    def get(self, menu_id):
        item = []
        for user in users_list:
            for menu in menu_list:
                if menu.id == menu_id:
                    menu_data = {}
                    menu_data["id"] = menu.id
                    menu_data["menu__name"] = menu.menu_name
                    item.append(menu_data)
            return make_response(jsonify({"menu_item": item[0]}), 200)
        return make_response(jsonify({"message": "Doesn't exist, Create an account please"}))


api.add_resource(Menus, '/api/v1/menu')


class MenuPost(Resource):
    def post(self, meal_id):
        for user in users_list:
            admin = user.isAdmin
            if admin == "True":
                for meal in meals_list:
                    if meal_id == meal.id:
                        menu_list.append(meal)
                        return make_response(jsonify({"message": "Meal successfully added to menu",
                                                      "status": "success"}), 201)
                    return make_response(jsonify({"meassage": "Meal does not exist"}))
            return make_response(jsonify({"message": "Customer is not allowed to do this"}), 400)


api.add_resource(MenuPost, '/api/v1/menu/<meal_id>')
