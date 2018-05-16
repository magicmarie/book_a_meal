""" control properties of the menu object"""
import uuid
import json


class Menu:
    def __init__(self, meals):
        self.id = uuid.uuid4().hex
        self.meals = meals

    def json(self):
        """
        json representation of the Menu model
        """
        return json.dumps({
            'id': self.id,
            'meal': self.meals
        })
