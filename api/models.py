"""control properties of the user, order, meal and menu objects"""

import json
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
    password = DB.Column(DB.String(25))
    is_admin = DB.Column(DB.String, default=False)

    def __init__(self, name, email, password, is_admin):
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        """defines the representation of an object"""
        return "id:{} name:{} email:{} is_admin:{}".format(self.id,
                                                           self.name,
                                                           self.email,
                                                           self.is_admin)#pragma:no cover

    def validate_input(self):
        """function to validate  sign up details"""
        if self.name.strip() == "" or len(self.name.strip()) < 3:
            return {"status": False, "message": "Enter name with more than 2 characters"}
        if not bool(re.fullmatch('^[A-Za-z ]*$', self.name)):
            return {"status": False, "message": "Invalid characters not allowed"}

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", self.email):
            return {"status": False, "message": "Enter valid email"}

        if self.password.strip() == "":
            return {"status": False, "message": "Enter password"}

        if len(self.password) < 5:
            return {"status": False, "message": "Enter password with more than 4 characters"}
        return {"status":True}

    def save(self):
        """
        saves the user to the DB
        """
        new_user = User(self.name, self.email, self.password, self.is_admin)    
        user = User.query.filter_by(email=self.email).first()
        if user:
            return {
                    "status": False,
                    "exists": True,
                    "message": "email already in use"
                }
        DB.session.add(new_user)
        DB.session.commit()
        return {"status": True, "message": "User successfully created"}

    @classmethod
    def log_user(cls, email, password):
        """
        logs in the user
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return {
                "status": False,
                "message": "User does not exist"
            }
        if email == user.email and password == user.password:
            access_token = "{}".format(
                generate_token(user.id, user.is_admin))
            return {
                "status": True,
                "token": access_token,
                "message": "User logged in successfully"
            }
        return {
            "status": False,
            "message": "wrong password credentials"
        }

    @classmethod
    def user_is_admin(cls, res):
        """
        Test for admin is True
        """
        user = User.query.filter_by(id=res['decoded']['id'], is_admin="True").first()
        if not user:
            return {
                "status": False,
                "message": "Customer is not authorized to access this page",
            }
        return {
            "status": True,
        }

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
        """defines the representation of an object"""
        return "id:{} mealId:{} userId:{}".format(self.orderId,
                                                  self.mealId,
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
        """defines the representation of an object"""
        return "id:{} meal_name:{} price:{} userId:{}".format(self.id,
                                                              self.meal_name,
                                                              self.price,
                                                              self.userId)#pragma:no cover
    
    def validate_inputs(self):
        """function to validate meal details"""
        if self.meal_name.strip() == "" or len(self.meal_name.strip()) < 3:
            return {"status": False, "message": "Enter meal name with more than 2 characters"}

        if not bool(re.fullmatch('^[A-Za-z ]*$', self.meal_name)):
            return {"status": False, "message": "Invalid characters not allowed"}
        return{"status": True}

    @classmethod
    def get_meals(cls, res):
        meals = cls.query.filter_by(userId=res['decoded']['id']).all()
        return meals

    @staticmethod
    def meals_serializer(meals):
        meal_items = []
        for meal in meals:
            meal_data = {
                "id": meal.id,
                "price": meal.price,
                "meal_name": meal.meal_name,
                "userId": meal.userId
            }
            meal_items.append(meal_data)
        return meal_items

    def save_meal(self, meal_name, price, res):
        meal = self.query.filter_by(meal_name=meal_name, userId=res['decoded']['id']).first()
        if meal:
            return {
                "status": False,
                "message": 'Meal name already exists'
            } 
        self.meal_name = meal_name
        self.price = price
        self.userId = res['decoded']['id']   
        DB.session.add(self)
        DB. session.commit()
        return {
            "status": True,
            'message': 'Meal successfully created'
        }

    @classmethod
    def find_meal(cls, meal_id, res):
        meal = Meal.query.filter_by(userId=res['decoded']['id'], id=meal_id).first()
        if not meal:
            return {
                "status": False,
                "message": "Meal not found"
            }
        return {
            "status": True,
            "meal": meal
        }
    
    def edit_meal(self, meal_name, price):
        self.meal_name = meal_name
        self.price = price
        DB.session.commit()
        return {
            "status": True,
            "message": "Meal updated succesfully"
        }


class Menu(DB.Model):
    """ control properties of the menu object"""
    __tablename__ = "menus"
    id = DB.Column(DB.Integer, primary_key=True)
    mealId = DB.Column(DB.Integer, DB.ForeignKey("meals.id"))
    meal = DB.relationship('Meal', backref='menus')

    def __repr__(self):
        """defines the representation of an object"""
        return "id:{} mealId:{}".format(self.id, self.mealId)#pragma:no cover

    def save_menu(self, meal_id, res):
        meal = self.query.filter_by(mealId=meal_id, userId=res['decoded']["id"]).first()
        if not meal:
            menu = self(mealId=meal_id)
            DB.session.add(menu)
            DB.session.commit()
            return {
                "status": True,
                "message": "Meal successfully added to menu"
            }
        return {
            "message": False,
            "message": "Meal already exists in menu"
        }
    
    @classmethod
    def get_menu(cls, res):
        user = User.query.filter_by(id=res['decoded']['id']).first()
        if not user: 
            menu = Menu.query.all()
            menu_items = []
            if menu:
                for menu_item in menu:
                    menu_data = {
                        "meal_id": menu_item.meal.id,
                        "meal_name": menu_item.meal.meal_name,
                        "price": menu_item.meal.price
                    }
                    menu_items.append(menu_data)
                return {
                    "status": True,
                    "menu": menu_items
                }


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
