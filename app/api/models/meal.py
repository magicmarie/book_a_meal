""" control properties of the meal object"""
import uuid
import re
import json


class Meal:
    def __init__(self, meal_name, price):
        self.id = uuid.uuid4().hex
        self.meal_name = meal_name
        self.price = price

    def json(self):
        """
        json representation of the Meal model
        """
        return json.dumps({
            'id': self.id,
            'meal_name': self.meal_name,
            'price': self.price
        })


def validate_inputs(meal_name=""):
    if meal_name.strip() == "" or len(meal_name.strip()) < 2:
        return {"status": False, "message": "invalid, Enter name please"}
        
    if not bool(re.fullmatch('^[A-Za-z ]*$', meal_name)):
        return {"status": False,"message": "Invalid characters not allowed"}
    return{"status": True}