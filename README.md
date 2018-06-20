[![Build Status](https://travis-ci.org/magicmarie/book_a_meal.svg?branch=flask%3Dapi-databases)](https://travis-ci.org/magicmarie/book_a_meal)
[![Coverage Status](https://coveralls.io/repos/github/magicmarie/book_a_meal/badge.svg?branch=flask%3Dapi-databases)](https://coveralls.io/github/magicmarie/book_a_meal?branch=flask%3Dapi-databases)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9c86a6940c82472ea181f0adecd25390)](https://www.codacy.com/app/magicmarie/book_a_meal?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=magicmarie/book_a_meal&amp;utm_campaign=Badge_Grade)


Book A Meal  is a web application  that allows customers to make food orders and
helps the food vendor to know what the customers want to eat.

This API is currently hosted on heroku https://book-a-meal-api-db.herokuapp.com/apidocs/#/

## Features
The application has a couple of features as listed below:-
 * Users can create an account and log in
 * Admin (Caterer) should be able to manage (i.e: add, modify and delete) meal options in the application. Examples of meal options are: Beef with rice, Beef with fries etc
 * Admin (Caterer) should be able to setup menu for a specific day by selecting from the meal options available on the system.
 * Authenticated users (customers) should be able to see the menu for a specific day and select an option out of the menu.
 * Authenticated users (customers) should be able to change their meal choice.
 * Admin (Caterer) should be able to see the orders made by the user
 * Admin should be able to see amount of money made by end of day
 * Authenticated users (customers) should be able to see their order history
 * Authenticated users (customers) should be able to get notifications when the menu for the day has been set.
 * Admin (Caterer) should be able to see order history
 * The application should be able to host more than one caterer.


## Setup
First clone it to your local machine by running

```
git clone https://github.com/magicmarie/book_a_meal.git
cd book_a_meal
```
## Starting the application
In order to run the application, run the command below to start the application.
```
python run.py
```
##How to setup the API backend
For windows

Prerequisites

a. Git

b. python 3.6 or higher

c. Install pip here

d. To install virtual environment: pip install virtualenv

e. To setup virtual environment: virtualenv venv

f. To activate virtual environment: venv\Scripts\activate

## API End points

| EndPoint                       | Method |
| ------------------------------ | ------ |
| `/api/v1/auth/signup`          | POST   |
| `/api/v1/auth/login`           | POST   |
| `/api/v1/meals`                | GET    |
| `/api/v1/meals`                | POST   |
| `/api/v1/meals/<int:mealId>`   | DELETE |
| `/api/v1/meals/<int:mealId>`   | PUT    |
| `/api/v1/menu`                 | GET    |
| `/api/v1/menu/<int:meal_id>`   | POST   |
| `/api/v1/orders`               | GET    |
| `/api/v1/orders<meal_id>`      | POST   |
| `/api/v1/user/orders`          | GET    |

1.  Test the endpoints using Postman

2.  To test the endpoints Run `pytest test`

