from flask import Flask
from flask_restful import Api

# Third party imports
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)


class User():
    usersArray = [
        {
            "name": "mariam",
            "email": "marie@gmail.com",
            "password": "mariam",
            "isAdmin": True
        },
        {
            "name": "aine",
            "email": "aine@gmail.com",
            "password": "aine",
            "isAdmin": False
        }
    ]

    def signup(self, name, email, password):
        for user in self.usersArray:
            if email = user["email"]:
                return{"success": False, "msg": "email in use"}
                self.users.append(user)

    def login(self, email, password):
        """account login """

        if email in self.usersArray:
            hashed_pswd = self.app_users[email].password
            if check_password_hash(hashed_pswd, password):
                return self.usersArray[email]
            return "Wrong email/password"
        return "The email does not exist, please signup"

    def get_user_info(self, email):
        for user in self.usersArray
        pass
