""" control properties of the menu object"""
import uuid
import json


class Menu:
    def __init__(self, menu_name):
        self.id = uuid.uuid4().hex
        self.meals = meals

    def json(self):
        return json.dumps({
            'id': self.id,
            'meals': self.meals
        })
