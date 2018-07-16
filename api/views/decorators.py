from flask import request, g
from api.auth_token import decode_token
from flask_restful import abort
from functools import wraps


def authenticate(func):
    """
    authenticate. protects a route to only authenticated users
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('token', '')
        if access_token.strip(' '):
            decoded = decode_token(access_token)
            if decoded['status']:
                return func(*args, **kwargs)
            abort(http_status_code=401, message='Invalid token.Please login')
        abort(http_status_code=401,
              message='Token is missing')
    return wrapper


def admin_required(func):
    """
    Protects admin routes
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if g.user["is_admin"] == "False":
            abort(http_status_code=401,
                  message='Customer is not authorized to access this page')
        return func(*args, **kwargs)
    return decorated_function
