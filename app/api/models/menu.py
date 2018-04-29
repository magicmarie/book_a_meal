""" control properties of the menu object"""
import uuid


class Menu:
    def __init__(self, menu_name):
        self.id = uuid.uuid4().hex
        self.menu_name = menu_name

    def __str__(self):
        return self.menu_name
