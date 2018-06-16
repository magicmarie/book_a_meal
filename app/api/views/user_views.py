""" user views"""
import json
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from app.api.models.user import User, generate_token, validate_input
from . import users

users_list = []
meals_list = []
menu_list = []
order_list = []

api = Api(users)


class Signup(Resource):
    """signup class"""
    @staticmethod
    @swag_from('../apidocs/signup.yml')
    def post():
        """
        Allows users(admins and customers) to create accounts
        """

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('is_admin', type=str, required=True)

        args = parser.parse_args()
        name = args['name']
        email = args['email']
        password = args['password']
        is_admin = args['is_admin']

        response = validate_input(name, email, password)
        if not response['status']:
            return make_response(jsonify({
                "message": response['message']
            }), 401)

        new_user = User(name, email, password, is_admin)

        for user in users_list:
            if email == user['email']:
                return make_response(jsonify({
                    "message": "email already in use"
                }), 400)

        users_list.append(json.loads(new_user.json()))
        return make_response(jsonify({
            'message': 'User successfully created'
        }), 201)

api.add_resource(Signup, '/api/v1/auth/signup')


class Login(Resource):
    """Login class"""
    @staticmethod
    @swag_from('../apidocs/login.yml')
    def post():
        """
        Allows users to login to their accounts
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        args = parser.parse_args()
        email = args['email']
        password = args['password']

        for user in users_list:
            if email == user['email'] and password == user['password']:
                access_token = "{}".format(
                    generate_token(user['id'], user['is_admin']))
                return make_response(jsonify({"token": access_token,
                                              "message": "User logged in successfully"
                                              }), 200)
        return make_response(jsonify({"message": "wrong credentials"}), 401)


api.add_resource(Login, '/api/v1/auth/login')
