"""control properties of the menu object"""
from api import DB


class Menu(DB.Model):
    """ control properties of the menu object"""
    __tablename__ = "menus"
    id = DB.Column(DB.Integer, primary_key=True)
    menu_name = DB.Column(DB.String(10))
    admin_id = DB.Column(DB.Integer)
    meal_id = DB.Column(DB.Integer, DB.ForeignKey("meals.id"))
    meals = DB.relationship('Meal', backref=DB.backref(
        "menus", cascade="all, delete-orphan"))

    def __repr__(self):
        """defines the representation of an object"""
        return "id:{} meal_id:{} menu_name:{}".format(
            self.id, self.meal_id, self.menu_name)  # pragma:no cover

    def save_menu(self, meal_id, res):
        menu_item = Menu.query.filter_by(
            meal_id=meal_id, menu_name=self.menu_name).first()
        if not menu_item:
            self.meal_id = meal_id
            self.admin_id = res["id"]
            DB.session.add(self)
            DB.session.commit()
            return {"status": True}
        return {"status": False}

    def find_menu_meal(self, menu_id, res):
        menu_item = self.query.filter_by(
            id=menu_id,
            admin_id=res['id']).first()
        if not menu_item:
            return {"status": False}
        return {"status": True,
                "meal": menu_item}
