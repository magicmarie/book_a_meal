"""control properties of the user, order, meal and menu objects"""
import re
from datetime import datetime, timedelta
import jwt

from flask import current_app
from api import DB, APP

class User(DB.Model):
    """ control properties of the user object"""
    __tablename__ = "users"
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(50))
    email = DB.Column(DB.String, unique=True)
    password = DB.Column(DB.String)
    is_admin = DB.Column(DB.String, default=False)

    def __init__(self, name, email, password, is_admin):
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        """defines the representation of an object"""
        return "id:{} name:{} email:{} is_admin:{}".format(self.id,#pragma:no cover
                                                           self.name,#pragma:no cover
                                                           self.email,#pragma:no cover
                                                           self.is_admin)#pragma:no cover


class Order(DB.Model):
    """ control properties of the order object"""
    __tablename__ = "orders"
    id = DB.Column(DB.Integer, primary_key=True)
    mealId = DB.Column(DB.Integer, DB.ForeignKey("meals.id"))
    userId = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    adminId = DB.Column(DB.Integer)
    user = DB.relationship('User', backref='orders')
    meal = DB.relationship('Meal', backref='orders')

    def __repr__(self):
        return "id:{} mealId:{} userId:{}".format(self.orderId,#pragma:no cover
                                                  self.mealId,#pragma:no cover
                                                  self.userId)#pragma:no cover


class Meal(DB.Model):
    """ control properties of the meal object"""
    __tablename__ = "meals"
    id = DB.Column(DB.Integer, primary_key=True)
    meal_name = DB.Column(DB.String(50))
    price = DB.Column(DB.Integer)
    userId = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    user = DB.relationship('User', backref='meals')

    def __repr__(self):
        return "id:{} meal_name:{} price:{} userId:{}".format(self.id,#pragma:no cover
                                                              self.meal_name,#pragma:no cover
                                                              self.price,#pragma:no cover
                                                              self.userId)#pragma:no cover


class Menu(DB.Model):
    """ control properties of the menu object"""
    __tablename__ = "menus"
    id = DB.Column(DB.Integer, primary_key=True)
    mealId = DB.Column(DB.Integer, DB.ForeignKey("meals.id"))
    meal = DB.relationship('Meal', backref='menus')

    def __repr__(self):
        return "id:{} mealId:{}".format(self.id, self.mealId)#pragma:no cover

def use_token(parser):
    """function to check for token"""
    parser.add_argument('token', location='headers')
    args = parser.parse_args()
    if not args['token']:
        return {"status": False, "message": "Token is missing"}
    decoded = decode_token(args['token'])
    if decoded["status"] == "Failure":
        return {"status": False, "message": decoded["message"]}
    return {"status": True, "decoded": decoded}


def validate_input(name="", email="", password=""):
    """function to validate  sign up details"""
    if name.strip() == "" or len(name.strip()) < 2:
        return {"status": False, "message": "invalid, Enter name please"}

    if not bool(re.fullmatch('^[A-Za-z ]*$', name)):
        return {"status": False, "message": "Invalid characters not allowed"}

    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        return {"status": False, "message": "Enter valid email"}

    if password.strip() == "":
        return {"status": False, "message": "Enter password"}

    if len(password) < 5:
        return {"status": False, "message": "Password is too short, < 5"}
    return {"status":True}

def validate_inputs(meal_name=""):
    """function to validate meal details"""
    if meal_name.strip() == "" or len(meal_name.strip()) < 2:
        return {"status": False, "message": "invalid, Enter meal name please"}

    if not bool(re.fullmatch('^[A-Za-z ]*$', meal_name)):
        return {"status": False, "message": "Invalid characters not allowed"}
    return{"status": True}

def generate_token(user_id, is_admin):
    """Generates the access token to be used as the Authorization header"""

    try:
        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=60),
            # international atomic time
            'iat': datetime.utcnow(),
            # default  to user id
            'sub': user_id,
            'is_admin': is_admin
        }
        # create the byte string token using the payload and the SECRET key
        jwt_string = jwt.encode(
            payload,
            APP.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('UTF-8')
        return jwt_string

    except Exception as e:#pragma:no cover
        # return an error in string format if an exception occurs
        return str(e)#pragma:no cover


def decode_token(token):
    """
    Decode the access token to get the payload and
    return user_id and is_admin field results
    """
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        return {
            "id": payload['sub'],
            "is_admin": payload['is_admin'],
            "status": "Success"
        }
    except jwt.InvalidTokenError:
        return {
            "status": "Failure",
            "message": "Invalid token.Please login"
        }
