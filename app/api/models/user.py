""" control properties of the user object"""
import uuid
import jwt
from datetime import datetime, timedelta
from flask import current_app


class User:
    def __init__(self, name, email, password, confirm_password, isAdmin):
        self.id = uuid.uuid4().int
        self.name = name
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.isAdmin = isAdmin

    def __str__(self):
        return self.name

    def generate_token(self, user_id):
        """Generates the access token to be used as the Authorization header"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=30),
                # international atomic time
                'iat': datetime.utcnow(),
                # default  to user id
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            ).decode('utf-8')
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
