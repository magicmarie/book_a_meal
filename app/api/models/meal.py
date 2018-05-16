""" control properties of the meal object"""
import uuid
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
