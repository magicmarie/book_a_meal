[![Build Status](https://travis-ci.org/magicmarie/book_a_meal.svg?branch=flaskAPI)](https://travis-ci.org/magicmarie/book_a_meal/)
Book A Meal  is a web application  that allows customers to make food orders and
helps the food vendor to know what the customers want to eat.
## Features
The application has a couple of features as listed below:-
 *Users can create an account and log in
 *Admin (Caterer) should be able to manage (i.e: add, modify and delete) meal options in the application. Examples of meal options are: Beef with rice, Beef with fries etc
 *Admin (Caterer) should be able to setup menu for a specific day by selecting from the meal options available on the system.
 *Authenticated users (customers) should be able to see the menu for a specific day and select an option out of the menu.
 *Authenticated users (customers) should be able to change their meal choice.
 *Admin (Caterer) should be able to see the orders made by the user
 *Admin should be able to see amount of money made by end of day
 *Authenticated users (customers) should be able to see their order history
 *Authenticated users (customers) should be able to get notifications when the menu for the day has been set.
 *Admin (Caterer) should be able to see order history
 *The application should be able to host more than one caterer.


## Setup
First clone it to your local machine by running

```
git clone https://github.com/magicmarie/book_a_meal.git
cd book_a_meal
```
## Starting the application
In order to run the application set the environment
variable below.
```
Windows
set FLASK_APP=run.py

Unix
export FLASK_APP=run.py
```
Then run the command below to start the application.
```
python run.py
```