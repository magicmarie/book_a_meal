"""control properties of the user, order, meal and menu objects"""
from api import DB
import jwt
import uuid
from datetime import datetime, timedelta
from flask import current_app


class User(DB.Model):
    __tablename__ = "users"
    id = DB.Column(DB.Integer, primary_key=True)
    userId = DB.Column(DB.Integer, unique=True)
    name = DB.Column(DB.String(50))
    email = DB.Column(DB.String, unique=True)
    password = DB.Column(DB.String)
    isAdmin = DB.Column(DB.Boolean, default=False)
    orders = DB.relationship('Order', backref='users')
    meals = DB.relationship('Meal', backref='users')

    def __repr__(self):
        return "userId:{} name:{} email:{} isAdmin:{} orders:{}".format(self.userId, self.name, self.email, self.isAdmin, self.orders)


class Order(DB.Model):
    __tablename__ = "orders"
    id = DB.Column(DB.Integer, primary_key=True)
    orderId = DB.Column(DB.Integer, unique=True)
    mealId = DB.Column(DB.String(50))
    userId = DB.Column(DB.Integer, DB.ForeignKey("users.userId"))
    menuName = DB.Column(DB.String(50), DB.ForeignKey("menus.menuName"))

    def __repr__(self):
        return "orderId:{} mealId:{} userId:{}".format(self.orderId, self.mealId, self.userId)


class Meal(DB.Model):
    __tablename__ = "meals"
    id = DB.Column(DB.Integer, primary_key=True)
    mealId = DB.Column(DB.Integer, unique=True)
    mealName = DB.Column(DB.String(50), unique=True)
    price = DB.Column(DB.Integer)
    userId = DB.Column(DB.Integer, DB.ForeignKey("users.userId"))
    menus = DB.relationship('Menu', backref='meals')

    def __repr__(self):
        return "mealId:{} mealName:{} price:{} userId:{} menus:{}".format(self.mealId, self.mealName, self.price, self.userId, self.menus)


class Menu(DB.Model):
    __tablename__ = "menus"
    id = DB.Column(DB.Integer, primary_key=True)
    menuId = DB.Column(DB.Integer, unique=True)
    menuName = DB.Column(DB.String(50))
    mealId = DB.Column(DB.Integer, DB.ForeignKey("meals.mealId"))
    orders = DB.relationship('Order', backref='menus')

    def __repr__(self):
        return "menuId:{} menuName:{} mealId:{} orders:{}".format(self.menuId, self.menuName, self.mealId, self.orders)


DB.create_all()


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
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ).decode('UTF-8')
        return jwt_string

    except Exception as e:
        # return an error in string format if an exception occurs
        return str(e)


def decode_token(token):
    """Decode the access token to get the payload and return user_id and isAdmin field results"""
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        return {"id": payload['sub'], "isAdmin": payload['isAdmin'], "status": "Success"}
    except jwt.ExpiredSignatureError:
        return {"status": "Failure", "message": "Expired token. Please log in to get a new token"}
    except jwt.InvalidTokenError:
        return {"status": "Failure", "message": "Invalid token. Please register or login"}
