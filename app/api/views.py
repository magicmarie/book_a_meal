# local imports
from app import app
from app import login_manager
from app.models.user import User
from app.models.menu import Menu
from app.models.meal import Meal
from app.models.order import Order
from app import login_manager


# t hird party imports
from .forms import LoginForm, SignupForm, MenuForm, MealForm
from flask import flash, render_template, url_for, redirect, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


# following https://somewebapp.com/api/v1/users
user1 = User()

# index


@app.route('/')
def index():
    return render_template('index.html')

# sign up a user


@app.route('/api/v1/auth/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        if email not in user1.usersArray:

            new_account = user1.signup(name, email, password)
            flash('Account has been created')
            if new_account:
                """ takes you to the login page """
                """ builds a URL for a specific function. The function accepts
                the name of a function as first argument corresponding to the
                variable part of URL."""
                return redirect(url_for('login'))
            flash('Account not created')
    """ Using the Jinja2 template engine to render an html file"""
    return render_template('signup.html', form=form)


@app.route('/api/v1/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email in user1.usersArray:
            loggedin = user1.login(email, password)

            if isinstance(loggedin, User1):
                login_user(loggedin)
                return redirect(url_for('account'))
    return render_template('login.html', form=form)


@app.route('/account')
@login_required
def admin():
    return render_template('account.html', category_data=category_data)

# get all meals


@app.route('/api/v1/meals', methods=['GET', 'POST'])
def get_meals():
    if request.method == 'GET':
        return render_template('admin.html')

# Add a meal


@app.route('/add_meal', methods=['GET', 'POST'])
@login_required
def add_meal():
    """" add_meal form"""
    form = MealForm()
    if form.validate_on_submit():
        meal_name = form.meal.data
        price = form.price.data
        meals[meal.name] = meals
        return redirect(url_for('admin'))
        return render_template('add_meal.html', form=form)

# update a meal


@app.route('/api/v1/meals/<int:mealid>', methods=['PUT'])
def update_meal():
    form = EditForm()
    pass


@app.route('/api/v1/meals/<int:mealid>', methods=['DELETE'])
def delete_meal():
    if meal_name in meals:
        del meals[meal_name]

# create menu


@app.route('/api/v1/menu', methods=['GET', 'POST'])
def create_menu():
    form = MenuForm()
    if form.validate_on_submit():
        menu_name = form.menu.data
    return render_template('admin/menu/add_menu.html')


# view order
@app.route('/api/v1/orders', methods=['GET', 'POST', 'PUT'])
def view_orders():
    if request.method == 'GET':
        return render_template('customer/menu1.html')
    else:
        pass

# update an order


@app.route('/api/v1/orders/<int:orderid>', methods=['PUT'])
def update_order():
    pass


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(email):
    return user1.usersArray.get(email)
