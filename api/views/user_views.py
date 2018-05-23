from flask import jsonify, make_response
from flask_restful import Resource, reqparse, Api
import re
import json
from . import users

from api.models import User, DB

api = Api(users)


class Signup(Resource):
    def post(self):
        """
        Allows users(admins and customers) to create accounts
        """

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('isAdmin', type=bool, required=True)

        args = parser.parse_args()
        name = args['name']
        email = args['email']
        password = args['password']
        isAdmin = args['isAdmin']

        if name.strip() == "" or len(name.strip()) < 2:
            return make_response(jsonify({"message": "invalid, Enter name please"}), 401)

        if re.compile('[!@#$%^&*:;?><.0-9]').match(name):
            return make_response(jsonify({"message": "Invalid characters not allowed"}))

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return make_response(jsonify({"message": "Enter valid email "}), 401)

        if password.strip() == "":
            return make_response(jsonify({"message": "Enter password"}), 401)

        if len(password) < 5:
            return make_response(jsonify({"message": "Password is too short, < 5"}), 401)

        user = User.query.filter_by(email=email).first()
        if not user:
            return make_response(jsonify({"message": "Email in use already"}))
        new_user = User(name=name, email=email,
                        password=password, isAdmin=isAdmin)
        print("mmmmmmmmmmmmmmmmmmmmm")
        DB.session.add(new_user)
        DB. session.commit()
        return make_response(jsonify({"status": "success", "message": "User successfully created"}), 201)


api.add_resource(Signup, '/api/v1/auth/signup')
