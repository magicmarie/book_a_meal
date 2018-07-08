[![Build Status](https://travis-ci.org/magicmarie/book_a_meal.svg?branch=flask%3Dapi-databases)](https://travis-ci.org/magicmarie/book_a_meal)
[![Coverage Status](https://coveralls.io/repos/github/magicmarie/book_a_meal/badge.svg?branch=flask%3Dapi-databases)](https://coveralls.io/github/magicmarie/book_a_meal?branch=flask%3Dapi-databases)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9c86a6940c82472ea181f0adecd25390)](https://www.codacy.com/app/magicmarie/book_a_meal?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=magicmarie/book_a_meal&amp;utm_campaign=Badge_Grade)


Book A Meal  is a web application  that allows customers to make food orders and
helps the food vendor to know what the customers want to eat.

*This API is currently hosted on heroku [url](https://book-a-meal-api-db.herokuapp.com/apidocs/#)*

## Requirements
- `Python3` - A programming language that lets us work more quickly.
- `Flask` - A microframework for Python based on Werkzeug, Jinja 2 and good intentions.
- `Virtualenv` - A tool to create an isolated virtual environment.
- `Git` - Versio Control System for tracking your changes.

## Setup
First clone it to your local machine by running
```
git clone https://github.com/magicmarie/book_a_meal.git
cd book_a_meal
```
Create virtual environment and activate it
```
$ virtualenv venv
$ source /venv/bin/activate
```
Then install all the necessary dependencies
```
pip install -r requirements.txt
```
## Set environment varibles and setup database
At the terminal or console type
```
export APP_SETTINGS=development
export DATABASE_URL=postgresql://postgres:magic@localhost/book_a_meal_db
psql -U postgres
postgres# CREATE ROLE postgres
postgres# CREATE DATABASE book_a_meal_db
```

## Initialize the database and create database tables
```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```
## Starting the application
In order to run the application, run the command below to start the application.
```
python run.py
```

## API End points
| EndPoint                       | Method | Functionality                                     | Access
| ------------------------------ | ------ | --------------------------------------------------| --------
| `/api/v1/auth/signup`          | POST   | Users(Admins and customers) can create an account | PUBLIC
| `/api/v1/auth/login`           | POST   | Users can log in to their accounts                | PUBLIC
| `/api/v1/meals`                | GET    | Admin can get all meal options he created         | PRIVATE
| `/api/v1/meals`                | POST   | Admin can add a meal option                       | PRIVATE 
| `/api/v1/meals/<int:meal_id>`   | DELETE | Admin can delete an existing meal by meal_id      | PRIVATE
| `/api/v1/meals/<int:meal_id>`   | PUT    | Admin can update an existing meal by meal_id      | PRIVATE
| `/api/v1/menu`                 | GET    | Users can get the menu                            | PRIVATE
| `/api/v1/menu/<int:meal_id>`   | POST   | Admin can add a meal he created to the menu by id | PRIVATE
| `/api/v1/orders`               | GET    | Admin can get all orders made on his meals        | PRIVATE
| `/api/v1/orders<meal_id>`      | POST   | User can make an order by meal_id                 | PRIVATE      
| `/api/v1/user/orders`          | GET    | Users can get all their orders                    | PRIVATE

Test the endpoints using Postman
*You could use a GUI platform like [postman](https://www.getpostman.com/) to make requests to and fro the api.*

To run tests run this command at the console/terminal
```
pytest tests
```
To run tests with coverage run this command at the console/terminal
```
pytest --cov=app
```

