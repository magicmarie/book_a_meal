import re
import uuid
import jwt
import datetime
import uuid
# t hird party imports
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, redirect, make_response, abort, session

# following https://somewebapp.com/api/v1/users
from . import api
from app import user_object
from app.models.user import User
# index


@api.route('/')
def index():
    return jsonify({"msg": "Welcome to Book-A-Meal"})

# sign up a user


@api.route('/api/v1/auth/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # passes in json data to the variable called data
        data = request.get_json(force=True)
        name = data['name']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        if name.strip() == "":
            error = {"message": "Invalid name"}
            return jsonify(error)
        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            error = {"message": "Invalid Email"}
            return jsonify(error)
        if password.strip() == "":
            error = {"message": "Invalid password"}
            return jsonify(error)
        if len(password) < 5:
            error = {"message": "Password too short"}
            return jsonify(error)
        if password != confirm_password:
            error = {"message": "passwords do not match"}
            return make_response(jsonify(error))

        # pass the details to the SIGNUP method
        result = user_object.signup(name, email, password, confirm_password)
        # print(result)
        if result:
            response = {
                "success": True,
                "message": "signup successful",
                "Data": data
            }
            return make_response(jsonify(response), 201)
        else:
            return make_response(jsonify({'message': 'user already exists'}), 200)


@api.route('/api/v1/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':  # POST request with valid input
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        result = user_object.login(email, password)

        if "email" == data["email"]:
            session['userid'] = result['id']
            session['email'] = email
            return jsonify(response="Login Successful"), 200
            token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)}, 'mariam', algorithm="HS256")
        if result:
            respond = {
                "success": True,
                "message": "Login successful",
                "Token": token.decode()
            }
            return jsonify(respond), 200
        return jsonify(response="Wrong Username or Password"), 401
