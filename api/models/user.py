"""control properties of the user object"""
import json
import re
from api import DB
from api.auth_token import generate_token


class User(DB.Model):
    """ control properties of the user object"""
    __tablename__ = "users"
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(25))
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
        return "id:{} name:{} email:{} is_admin:{}".format(
            self.id, self.name, self.email, self.is_admin)  # pragma:no cover

    def validate_input(self):
        """function to validate  sign up details"""
        if self.name.strip() == "" or len(self.name.strip()) < 3:
            return {
                "status": False,
                "message": "Enter name with more than 2 characters"}

        if len(self.name.strip()) > 25:
            return {
                "status": False,
                "message": "Enter name with less than 25 characters"}

        if not bool(re.fullmatch('^[A-Za-z ]*$', self.name)):
            return {
                "status": False,
                "message": "Invalid characters not allowed"}

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", self.email):
            return {"status": False, "message": "Enter valid email"}

        if self.password.strip() == "":
            return {"status": False, "message": "Enter password"}

        if len(self.password) < 5:
            return {
                "status": False,
                "message": "Enter password with more than 4 characters"}
        return {"status": True}

    def save(self):
        """
        saves the user to the DB
        """
        new_user = User(self.name, self.email, self.password, self.is_admin)
        user = User.query.filter_by(email=self.email).first()
        if user:
            return {"status": False}
        DB.session.add(new_user)
        DB.session.commit()
        return {"status": True}

    @classmethod
    def log_user(cls, email, password):
        """
        logs in the user
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return {
                "status": False,
                "exists": False
            }
        if email == user.email and password == user.password:
            access_token = "{}".format(
                generate_token(user.id, user.is_admin))
            return {
                "status": True,
                "token": access_token
            }
        return {"status": False, "exists": True}

    @classmethod
    def user_is_admin(cls, res):
        """
        Test for admin is True
        """
        user = User.query.filter_by(
            id=res['decoded']['id'],
            is_admin="True").first()
        if not user:
            return {
                "status": False,
                "message": "Customer is not authorized to access this page",
            }
        return {
            "status": True,
        }
