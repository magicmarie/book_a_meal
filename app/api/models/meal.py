""" control properties of the meal object"""
import uuid
import re
import json

meals_list = []


class Meal:
    """
    Class to represent the meal model
    """
    def __init__(self, meal_name, price, admin_id):
        self.id = uuid.uuid4().hex
        self.meal_name = meal_name
        self.price = price
        self.admin_id = admin_id

    def json(self):
        """
        json representation of the Meal model
        """
        return json.dumps({
            'id': self.id,
            'meal_name': self.meal_name,
            'price': self.price,
            'admin_id': self.admin_id
        })


    def validate_inputs(self):
        """
        validates user input
        """
        if self.meal_name.strip() == "" or len(self.meal_name.strip()) < 2:
            return {"status": False, "message": "invalid, Enter name please"}
        if len(self.meal_name.strip()) > 25:
            return {"status": False, "message": "Enter name not more than 25 characters"}
        if not bool(re.fullmatch('^[A-Za-z ]*$', self.meal_name)):
            return {"status": False, "message": "Invalid characters not allowed"}

        try:
            int(self.price)
        except ValueError:
            return {"status": False, "message": "Price must be a number"}
        return{"status": True}

    def save(self):
        """
        saves meal
        """
        new_meal = Meal(self.meal_name, self.price, self.admin_id)
        for meal in meals_list:
            if self.meal_name == meal.meal_name and self.admin_id == meal.admin_id:
                return {
                    'status': False, 'message': 'Meal name already exists'}
        meals_list.append(new_meal)
        return {'status': True, 'message': 'Meal successfully created'}

    @staticmethod
    def delete_meal(meal_id):
        """
        deletes a meal
        """
        for meal in meals_list:
            if meal.id == meal_id:
                meals_list.remove(meal)
                return {
                    "status": True,
                    "message": "Meal deleted succesfully"
                }
        return {"status": False,
            "message": "Meal not found"
        }