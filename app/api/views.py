import re
# t hird party imports
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, redirect, make_response, abort

# following https://somewebapp.com/api/v1/users
from . import api
from app import user_object
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

        # for user in user_object.usersArray:
        #     if user['email'] == email:
        #         return make_response(jsonify({'message': 'User already exists'}), 409)
        # # pass the details to the register method
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
