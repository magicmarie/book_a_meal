"""control properties of the menu object"""
from api import DB
from api.models.user import User


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
        meal = self.query.filter_by(
            meal_id=meal_id).first()
        if not meal:
            menu = self(meal_id=meal_id)
            DB.session.add(menu)
            DB.session.commit()
            return {"status": True}
        return {"status": False}

    @classmethod
    def get_menu(cls, res):
        user = User.query.filter_by(id=res['decoded']['id']).first()
        if user:
            menu = Menu.query.all()
            menu_items = []
            if menu:
                for menu_item in menu:
                    menu_data = {
                        "meal_id": menu_item.meal.id,
                        "meal_name": menu_item.meal.meal_name,
                        "price": menu_item.meal.price
                    }
                    menu_items.append(menu_data)
                return {"status": True, "menu": menu_items}
