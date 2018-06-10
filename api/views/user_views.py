import re
import json
import jwt
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
from flasgger.utils import swag_from

from . import users
from api.models import User, generate_token, decode_token
from api import DB

api = Api(users)


class Signup(Resource):
    @swag_from('../apidocs/signup.yml')
    def post(self):
        """
        Allows users(admins and customers) to create accounts
        """

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

        if name.strip() == "" or len(name.strip()) < 2:
            return make_response(jsonify({
                "message": "invalid, Enter name please"
            }), 401)

        if re.compile('[!@#$%^&*:;?><.0-9]').match(name):
            return make_response(jsonify({
                "message": "Invalid characters not allowed"
            }), 401)

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return make_response(jsonify({
                "message": "Enter valid email"
            }), 401)

        if password.strip() == "":
            return make_response(jsonify({
                "message": "Enter password"
            }), 401)

        if len(password) < 5:
            return make_response(jsonify({
                "message": "Password is too short, < 5"
            }), 401)

        user = User.query.filter_by(email=email).first()
        if user:
            return make_response(jsonify({
                "message": "Email in use already"
            }), 401)
        new_user = User(name=name, email=email,
                        password=password, isAdmin=isAdmin)
        DB.session.add(new_user)
        DB.session.commit()
        return make_response(jsonify({
            "status": "success",
            "message": "User successfully created"
        }), 201)


api.add_resource(Signup, '/api/v1/auth/signup')


class Login(Resource):
    @swag_from('../apidocs/login.yml')
    def post(self):
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
            }), 401)
        if email == user.email and password == user.password:
            access_token = generate_token(user.id, user.isAdmin)
            return make_response(jsonify({
                "token": access_token,
                "user_id": decode_token(access_token)['id'],
                "message": "User logged in successfully"
            }), 200)
        return make_response(jsonify({
            "message": "wrong password"
        }), 401)


api.add_resource(Login, '/api/v1/auth/login')
