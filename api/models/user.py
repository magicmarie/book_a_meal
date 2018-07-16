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
    is_admin = DB.Column(DB.String)

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
        status = True
        messages = []
        name = self.name.strip()
        if name == "" or len(name) < 3 or len(name) > 25:
            status = False
            messages.append("Name must be between 3 to 25 characters long")
        if not bool(re.fullmatch('^[A-Za-z ]*$', name)):
            status = False
            messages.append("Invalid characters not allowed")
        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", self.email):
            status = False
            messages.append("Enter valid email")
        if self.password.strip() == "" or len(self.password) < 5:
            status = False
            messages.append("Enter password with more than 5 characters")
        return {"status": status, "message": ", ".join(messages)}

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
