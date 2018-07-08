"""control properties of the meal object"""
import json
import re
from api import DB


class Meal(DB.Model):
    """ control properties of the meal object"""
    __tablename__ = "meals"
    id = DB.Column(DB.Integer, primary_key=True)
    meal_name = DB.Column(DB.String(25))
    price = DB.Column(DB.Integer)
    user_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    user = DB.relationship('User', backref='meals')

    def __repr__(self):
        """defines the representation of an object"""
        return "id:{} meal_name:{} price:{} user_id:{}".format(
            self.id, self.meal_name, self.price, self.user_id)  # pragma:no cover

    def validate_inputs(self):
        """function to validate meal details"""
        if self.meal_name.strip() == "" or len(self.meal_name.strip()) < 3:
            return {
                "status": False,
                "message": "Enter meal name with more than 2 characters"}

        if len(self.meal_name.strip()) > 25:
            return {
                "status": False,
                "message": "Enter meal name with less than 25 characters"}

        if not bool(re.fullmatch('^[A-Za-z ]*$', self.meal_name)):
            return {
                "status": False,
                "message": "Invalid characters not allowed"}

        if self.price <= "0":
            return {
                "status": False,
                'message': "Price must be a positive number"}
        try:
            int(self.price)
        except ValueError:
            return {"status": False, "message": "Price must be a number"}
        return{"status": True}

    @classmethod
    def get_meals(cls, res):
        meals = cls.query.filter_by(user_id=res['decoded']['id']).all()
        return meals

    @staticmethod
    def meals_serializer(meals):
        meal_items = []
        for meal in meals:
            meal_data = {
                "id": meal.id,
                "price": meal.price,
                "meal_name": meal.meal_name,
                "user_id": meal.user_id
            }
            meal_items.append(meal_data)
        return meal_items

    def save_meal(self, meal_name, price, res):
        meal = self.query.filter_by(
            meal_name=meal_name,
            user_id=res['decoded']['id']).first()
        if meal:
            return {"status": False}
        self.meal_name = meal_name
        self.price = price
        self.user_id = res['decoded']['id']
        DB.session.add(self)
        DB. session.commit()
        return {"status": True}

    @classmethod
    def find_meal(cls, meal_id, res):
        meal = Meal.query.filter_by(
            user_id=res['decoded']['id'],
            id=meal_id).first()
        if not meal:
            return {
                "status": False,
                "message": "Meal not found"
            }
        return {
            "status": True,
            "meal": meal
        }

    def edit_meal(self, meal_name, price):
        self.meal_name = meal_name
        self.price = price
        return {"status": True, "meal": self}
