""" control properties of the user object"""
import uuid
import re
import json
from datetime import datetime, timedelta
import jwt

from flask import current_app

users_list = []

class User:
    """
    Class to represent the User model
    """

    def __init__(self, name, email, password, is_admin):
        self.id = uuid.uuid4().int
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def json(self):
        """
        json representation of the User model
        """

        return json.dumps({
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'is_admin': self.is_admin
        })
    def save(self):
        """
        saves the user
        """
        new_user = json.loads(User(self.name, self.email, self.password, self.is_admin).json())
        for user in users_list:
            if self.email == user['email']:
                return {
                    "status": False,
                    "exists": True,
                    "message": "email already in use"
                }
        users_list.append(new_user)
        return {"status": True, "message": "User successfully created"}

    def validate_input(self):
        """
        validates the user input
        """
        if self.name.strip() == "" or len(self.name.strip()) < 3:
            return {
                "status": False,
                "message": "Enter name with more than 2 characters please"
            }

        if not bool(re.fullmatch('^[A-Za-z ]*$', self.name)):
            return {"status": False, "message": "Invalid characters not allowed"}

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", self.email):
            return {"status": False, "message": "Enter valid email "}

        if self.password.strip() == "":
            return {"status": False, "message": "Enter password"}

        if len(self.password) < 5:
            return {
                "status": False,
                "message": "Password is less than 5 characters"
            }
        return {"status":True}

    @staticmethod
    def log_user(email, password):
        """
        logs in the user
        """
        for user in users_list:
            if email == user['email'] and password == user['password']:
                access_token = "{}".format(
                    generate_token(user['id'], user['is_admin']))
                return {
                    "status": True,
                    "token": access_token,
                    "message": "User logged in successfully"
                }
        return {
            "status": False,
            "message": "wrong email or password credentials"
        }

def use_token(parser):
    """
    Function to test valid token
    """
    parser.add_argument('token', location='headers')
    args = parser.parse_args()
    if not args['token']:
        return {"status": False, "message": "Token is missing"}
    decoded = decode_token(args['token'])
    if decoded["status"] == "Failure":
        return {"status": False, "message": decoded["message"]}
    return {"status": True, "decoded": decoded}

def generate_token(user_id, is_admin):
    """Generates the access token to be used as the Authorization header"""

    try:
        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=30),
            # international atomic time
            'iat': datetime.utcnow(),
            # default  to user id
            'sub': user_id,
            'is_admin': is_admin
        }
        # create the byte string token using the payload and the SECRET key
        jwt_string = jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ).decode('UTF-8')
        return jwt_string

    except Exception as e:
        # return an error in string format if an exception occurs
        return str(e)


def decode_token(token):
    """Decode the access token to get the payload and return
     user_id and is_admin"""

    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        return {
            "id": payload['sub'],
            "is_admin": payload['is_admin'],
            "status": "Success"
        }
    except jwt.ExpiredSignatureError:
        return {
            "status": "Failure", 
            "message": "Expired token. Please log in to get a new token"
        }
    except jwt.InvalidTokenError:
        return {
            "status": "Failure", 
            "message": "Invalid token. Please register or login"
        }
