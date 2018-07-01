""" user views"""
import json
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from app.api.models.user import User
from . import users

api = Api(users)
meals_list = []
order_list = []
menu_list = []


class Signup(Resource):
    """signup class"""
    @staticmethod
    @swag_from('../apidocs/signup.yml')
    def post():
        """
        Allows users(admins and customers) to create accounts
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help="Name is required", required=True)
        parser.add_argument('email', type=str, help="EEmail is required", required=True)
        parser.add_argument('password', type=str, help="Password is required", required=True)
        parser.add_argument('is_admin', type=str, help="is_admin is required", required=True)

        args = parser.parse_args()

        user = User(
            args['name'],
            args['email'],
            args['password'],
            args['is_admin'])
        res = user.validate_input()
        if not res['status']:
            return make_response(jsonify({
                'message': res["message"]
            }), 400)
        response = user.save()
        if "exists" in response and response["exists"]:
            return make_response(jsonify({
                'message': response["message"]
            }), 409)
        return make_response(jsonify({
            'message': response["message"]
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
        parser.add_argument('email')
        parser.add_argument('password')

        args = parser.parse_args()
        response = User.log_user(args['email'], args['password'])
        if response["status"]:
            return make_response(jsonify({
                'message': response["message"],
                'token': response['token']
            }), 200)
        return make_response(jsonify({
            'message': response["message"]
        }), 400)

api.add_resource(Login, '/api/v1/auth/login')
