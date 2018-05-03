from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api

import re
from . import users

from app.api.models.user import User, generate_token

users_list = []
meals_list = []
menu_list = []
order_list = []

api = Api(users)


class Signup(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('isAdmin', type=str, required=True)

        args = parser.parse_args()
        name = args['name']
        email = args['email']
        password = args['password']
        isAdmin = args['isAdmin']

        if name.strip() == "":
            return make_response(jsonify({"message": "invalid, Enter name please"}), 401)

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return make_response(jsonify({"message": "Enter valid email "}), 401)

        if password.strip() == "":
            return make_response(jsonify({"message": "Enter password"}), 401)

        if len(password) < 5:
            return make_response(jsonify({"message": "Password is too short, < 5"}), 401)

        new_user = User(name, email, password, isAdmin)

        for user in users_list:
            if email == user.email:
                return make_response(jsonify({"message": "email already in use"}), 400)

        users_list.append(new_user)
        return make_response(jsonify({'message': 'User successfully created'}), 201)


api.add_resource(Signup, '/api/v1/auth/signup')


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        args = parser.parse_args()
        email = args['email']
        password = args['password']

        for user in users_list:
            if email == user.email and password == user.password:
                access_token = "{}".format(generate_token(user.id))
                return make_response(jsonify({"token": access_token,
                                              "message": "User logged in successfully"
                                              }), 200)
        return make_response(jsonify({"message": "wrong credentials"}), 401)


api.add_resource(Login, '/api/v1/auth/login')