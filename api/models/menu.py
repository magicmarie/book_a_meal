"""control properties of the menu object"""
from api import DB
from api.models.user import User
from api.models.meal import Meal


class Menu(DB.Model):
    """ control properties of the menu object"""
    __tablename__ = "menus"
    id = DB.Column(DB.Integer, primary_key=True)
    meal_id = DB.Column(DB.Integer, DB.ForeignKey("meals.id"))
    meal = DB.relationship('Meal', backref='menus')

    def __repr__(self):
        """defines the representation of an object"""
        return "id:{} meal_id:{}".format(
            self.id, self.meal_id)  # pragma:no cover

    def save_menu(self, meal_id, res):
        menu_item = Menu.query.filter_by(
            meal_id=meal_id).first()
        if not menu_item:
            self.meal_id = meal_id
            DB.session.add(self)
            DB.session.commit()
            return {"status": True}
        return {"status": False}

    @classmethod
    def get_menu(cls, user):
        user = User.query.filter_by(id=user['id']).first()
        if user:
            menus = Menu.query.all()
            menu_items = []
            for menu_item in menus:
                meal = Meal.query.filter_by(id=menu_item.meal_id).first()
                menu_data = {
                    "id": menu_item.id,
                    "meal_id": menu_item.meal_id,
                    "meal_name": meal.meal_name,
                    "price": meal.price
                }
                menu_items.append(menu_data)
            return {"status": True, "menu": menu_items}
