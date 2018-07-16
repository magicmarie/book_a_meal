""" user views"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api, fields, abort
from flasgger.utils import swag_from
from api.models.user import User
from . import api


class Signup(Resource):
    """sign up class"""
    @staticmethod
    @swag_from('../apidocs/signup.yml')
    def post():
        """
        Allows users(admins and customers) to create accounts
        """

        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', type=str, help="Name is a required field", required=True)
        parser.add_argument(
            'email', type=str, help="Email is a required field", required=True)
        parser.add_argument(
            'password', type=str, help="Password is a required field",
            required=True)
        parser.add_argument(
            'is_admin', type=str, help="is_admin is a required field",
            required=True)

        args = parser.parse_args()
        user = User(args['name'], args['email'], args['password'],
                    args['is_admin'])

        res = user.validate_input()
        if not res['status']:
            abort(http_status_code=400, message=res['message'])
        response = user.save()
        if not response['status']:
            abort(http_status_code=409, message="email already in use")
        return make_response(jsonify({
            "message": "User successfully created"
        }), 201)


class Login(Resource):
    """login class"""
    @staticmethod
    @swag_from('../apidocs/login.yml')
    def post():
        """
        Allows users to login to their accounts
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str,
                            help="Name is a required field", required=True)
        parser.add_argument('password', type=str,
                            help="Password is a required field",
                            required=True)
        args = parser.parse_args()
        response = User.log_user(args['email'], args['password'])
        if "exists" in response and not response["exists"]:
            abort(http_status_code=400, message="User does not exist")
        if "exists" in response and response["exists"]:
            abort(http_status_code=400,
                  message="wrong password or email credentials")
        return make_response(jsonify({
            'message': "User logged in successfully",
            'token': response['token']
        }), 200)
