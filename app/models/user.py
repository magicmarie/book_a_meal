"""defines a user class, methods associated to it"""
# used to validate names
import uuid
import jwt
from datetime import datetime, timedelta

# Third party imports
from werkzeug.security import generate_password_hash, check_password_hash

usersArray = list()
known_email = list()


class User(object):
    """ A class to handle activities related to a user"""

    def __init__(self):
        # A list to hold all user objects
        # self.usersArray = []
        pass

    # def generate_token(self, user_id):
    #     """Generates the access token to be used as the Authorization header"""
    #     try:     # set up a payload with an expiration time
    #         payload = {
    #             'exp': datetime.utcnow() + timedelta(minutes=30),
    #             # international atomic time
    #             'iat': datetime.utcnow(),
    #             # default  to user id
    #             'sub': user_id
    #         }
    #         # create the byte string token using the payload and the SECRET key
    #         jwt_string = jwt.encode(
    #             payload,
    #             'hard to guess string',
    #             algorithm='HS256'
    #         )
    #         return jwt_string

    #     except Exception as e:
    #         # return an error in string format if an exception occurs
    #         return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, 'hard to guess string')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"

    def signup(self, name, email, password, confirm_password):
        """method to sign up a user"""
        global usersArray
        global known_email
        # user_details = {}
        if email in known_email:
            return False
        else:
            user_details = dict()
            user_details['name'] = name
            user_details['email'] = email
            user_details['password'] = password
            user_details['confirm_password'] = confirm_password
            # uuid4 generates a random UUID
            user_details['id'] = uuid.uuid4()
            # print(user_details)
            usersArray.append(user_details)
            known_email.append(email)
            return True

    def login(self, email, password):
        """account login """
        if email in self.usersArray:
            hashed_pswd = self.usersArray[email].password
            if check_password_hash(hashed_pswd, password):
                return self.usersArray[email]
            return "Wrong email/password"
        return "The email does not exist, please signup"

    def get_user_info(self, id):
        """retrieve user by their id"""
        for user in self.usersArray:
            if user["id"] == user_id:
                return user
