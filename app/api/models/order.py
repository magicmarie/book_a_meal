""" control properties of the order object"""
import uuid


class Order:
    def __init__(self, order_name):
        self.id = uuid.uuid4().hex
        self.order_name = order_name

    def __str__(self):
        return self.order_name
