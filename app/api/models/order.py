""" control properties of the order object"""
import uuid
import json


class Order:
    def __init__(self, meal_id, user_id):
        self.id = uuid.uuid4().hex
        self.meal_id = meal_id
        self.user_id = user_id

    def json(self):
        """
        json representation of the Order model
        """
        return json.dumps({
            'id': self.id,
            'meal_id': self.meal_id,
            'user_id': self.user_id
        })
