""" control properties of the order object"""
import uuid


class Order:
    def __init__(self, meal_name, price):
        self.id = uuid.uuid4().hex
        self.meal_name = meal_name
        self.price = price

    def __str__(self):
        return self.meal_name
