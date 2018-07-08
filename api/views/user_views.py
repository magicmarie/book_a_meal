""" user views"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from api.models.user import User
from . import users

api = Api(users)


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
            'name',
            type=str,
            help="Name is a required field",
            required=True)
        parser.add_argument(
            'email',
            type=str,
            help="Email is a required field",
            required=True)
        parser.add_argument(
            'password',
            type=str,
            help="Password is a required field",
            required=True)
        parser.add_argument(
            'is_admin',
            type=str,
            help="is_admin is a required field",
            required=True)

        args = parser.parse_args()
        user = User(
            args['name'],
            args['email'],
            args['password'],
            args['is_admin'])

        res = user.validate_input()
        if not res['status']:
            return make_response(jsonify({
                "message": res['message']
            }), 400)

        response = user.save()
        if not response['status']:
            return make_response(jsonify({
                "message": "email already in use"
            }), 409)
        return make_response(jsonify({
            "message": "User successfully created"
        }), 201)


api.add_resource(Signup, '/api/v1/auth/signup')


class Login(Resource):
    """login class"""
    @staticmethod
    @swag_from('../apidocs/login.yml')
    def post():
        """
        Allows users to login to their accounts
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email',
            type=str,
            help="Name is a required field",
            required=True)
        parser.add_argument(
            'password',
            type=str,
            help="Password is a required field",
            required=True)

        args = parser.parse_args()

        response = User.log_user(args['email'], args['password'])
        if "exists" in response and not response["exists"]:
            return make_response(jsonify({
                'message': "User does not exist"
            }), 400)
        if "exists" in response and response["exists"]:
            return make_response(jsonify({
                'message': "wrong password or email credentials"
            }), 400)
        return make_response(jsonify({
            'message': "User logged in successfully",
            'token': response['token']
        }), 200) 


api.add_resource(Login, '/api/v1/auth/login')
