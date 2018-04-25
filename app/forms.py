# local imports
from app.models.meal import Meal
from app.models.menu import Menu
from app.models.user import User
from app.models.order import Order

# third party imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    # Users log into their accounts
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SignupForm(FlaskForm):
    # This allows users to create accounts
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', [validators.Required(
    ), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    """print("....", name, email, password, confirm)"""


class EditForm(FlaskForm):
    # Editing the meal
    meal = StringField('meal:', validators=[DataRequired()])
    price = IntegerField('price:', validators=[DataRequired()])


class MenuForm(FlaskForm):
    # creates a menu
    menu = StringField('menu:', validators=[DataRequired()])


class MealForm(FlaskForm):
    # creates a meal
    meal = StringField('meal:', validators=[DataRequired()])
    price = IntegerField('price:', validators=[DataRequired()])
