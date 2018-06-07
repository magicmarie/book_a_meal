"""control properties of the user, order, meal and menu objects"""
from api import DB, APP
import jwt
from datetime import datetime, timedelta
from flask import current_app


class User(DB.Model):
    __tablename__ = "users"
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(50))
    email = DB.Column(DB.String, unique=True)
    password = DB.Column(DB.String)
    isAdmin = DB.Column(DB.String, default=False)

    def __init__(self, name, email, password, isAdmin):
        self.name = name
        self.email = email
        self.password = password
        self.isAdmin = isAdmin

    def __repr__(self):
        """defines the representation of an object"""
        return "id:{} name:{} email:{} isAdmin:{}".format(self.userId,
                                                          self.name,
                                                          self.email,
                                                          self.isAdmin)


class Order(DB.Model):
    __tablename__ = "orders"
    id = DB.Column(DB.Integer, primary_key=True)
    mealId = DB.Column(DB.String(50))
    userId = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    adminId = DB.Column(DB.Integer, DB.ForeignKey("meals.userId"))
    user = DB.relationship('User', backref='orders')
    admin = DB.relationship('Meal', backref='orders')

    def __repr__(self):
        return "id:{} mealId:{} userId:{}".format(self.orderId,
                                                  self.mealId,
                                                  self.userId)


class Meal(DB.Model):
    __tablename__ = "meals"
    id = DB.Column(DB.Integer, primary_key=True)
    meal_name = DB.Column(DB.String(50), unique=True)
    price = DB.Column(DB.Integer)
    userId = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    user = DB.relationship('User', backref='meals')

    def __repr__(self):
        return "id:{} meal_name:{} price:{} userId:{}".format(self.id,
                                                              self.meal_name,
                                                              self.price,
                                                              self.userId)


class Menu(DB.Model):
    __tablename__ = "menus"
    id = DB.Column(DB.Integer, primary_key=True)
    mealId = DB.Column(DB.Integer, DB.ForeignKey("meals.id"))
    meal = DB.relationship('Meal', backref='menus')

    def __repr__(self):
        return "id:{} mealId:{}".format(self.id, self.mealId)


def generate_token(user_id, isAdmin):
    """Generates the access token to be used as the Authorization header"""

    try:
        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=60),
            # international atomic time
            'iat': datetime.utcnow(),
            # default  to user id
            'sub': user_id,
            'isAdmin': isAdmin
        }
        # create the byte string token using the payload and the SECRET key
        jwt_string = jwt.encode(
            payload,
            APP.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('UTF-8')
        return jwt_string

    except Exception as e:
        # return an error in string format if an exception occurs
        return str(e)


def decode_token(token):
    """
    Decode the access token to get the payload and
    return user_id and isAdmin field results
    """
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        return {
            "id": payload['sub'],
            "isAdmin": payload['isAdmin'],
            "status": "Success"
        }
    except jwt.InvalidTokenError:
        return {
            "status": "Failure",
            "message": "Invalid token.Please login"
        }
