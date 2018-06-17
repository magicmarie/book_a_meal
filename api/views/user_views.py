""" user views"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from api.models import User, generate_token, decode_token, validate_input
from api import DB
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

        user = User.query.filter_by(email=email).first()
        if user:
            return make_response(jsonify({
                "message": "Email in use already"
            }), 401)
        new_user = User(name=name, email=email,
                        password=password, is_admin=is_admin)
        DB.session.add(new_user)
        DB.session.commit()
        return make_response(jsonify({
            "status": "success",
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
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        args = parser.parse_args()
        email = args['email']
        password = args['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            return make_response(jsonify({
                "message": "User does not exist"
            }), 400)
        if email == user.email and password == user.password:
            access_token = generate_token(user.id, user.is_admin)
            return make_response(jsonify({
                "token": access_token,
                "message": "User logged in successfully"
            }), 200)
        return make_response(jsonify({
            "message": "wrong email or password"
        }), 400)


api.add_resource(Login, '/api/v1/auth/login')
