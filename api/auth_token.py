"""generate and decode token"""
from datetime import datetime, timedelta
import jwt
from flask import current_app, g
from api import APP


def generate_token(user_id, email, is_admin):
    """Generates the access token to be used as the Auth header"""

    try:
        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=60),
            # international atomic time
            'iat': datetime.utcnow(),
            # default  to user id
            'sub': user_id,
            'email': email,
            'is_admin': is_admin
        }
        # create the byte string token using the payload and the SECRET key
        jwt_string = jwt.encode(
            payload,
            APP.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('UTF-8')
        return jwt_string

    except Exception as e:  # pragma:no cover
        # return an error in string format if an exception occurs
        return str(e)  # pragma:no cover


def decode_token(token):
    """
    Decode the access token to get the payload and
    return user_id and is_admin field results
    """
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        user = {
            "status": True,
            "id": payload['sub'],
            "email": payload['email'],
            "is_admin": payload['is_admin']
        }
        # add user to the context
        g.user = user
        return user
    except jwt.InvalidTokenError:
        return {
            "status": False,
            "message": "Invalid token.Please login"
        }
