"""control properties of the order object"""
from api import DB
from api.models.menu import Menu
from api.models.meal import Meal


class Order(DB.Model):
    """ control properties of the order object"""
    __tablename__ = "orders"
    id = DB.Column(DB.Integer, primary_key=True)
    meal_id = DB.Column(DB.Integer, DB.ForeignKey("meals.id"))
    customer_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    admin_id = DB.Column(DB.Integer)
    user = DB.relationship('User', backref='orders')
    meal = DB.relationship('Meal', backref='orders')

    def __repr__(self):
        """defines the representation of an object"""
        return "id:{} meal_id:{} user_id:{} admin_id:{}".format(
            self.id, self.meal_id, self.customer_id, self.admin_id)  # pragma:no cover

    def add_order(self, res, menu_id, meal_id):
        order = Menu.query.filter_by(id=menu_id, meal_id=meal_id).first()
        if not order:
            return {"status": False}
        meal = Meal.query.filter_by(id=meal_id).first()
        self.meal_id=meal_id,
        self.customer_id=res['decoded']['id'],
        self.admin_id=meal.user_id
        DB.session.add(self)
        DB.session.commit()
        return {'status': True}

    def get_admin_orders(self, res):
        total = 0
        orderz = self.query.filter_by(admin_id=res['decoded']['id']).all()
        if orderz:
            order_items = []
            for order in orderz:
                meal = Meal.query.filter_by(id=order.meal_id).first()
                order_data = {
                    "id": order.id,
                    "meal_id": order.meal_id,
                    "user_id": order.customer_id,
                    "meal_name": meal.meal_name,
                    "price": meal.price
                }
                order_items.append(order_data)
                total += order.meal.price
            return {
                'status': True,
                "order_items": order_items,
                "total": total
            }
        return {'status': False}

    def get_user_orders(self, res):
        order = self.query.filter_by(customer_id=res['decoded']['id']).all()
        user_order_items = []
        total = 0
        if not order:
            return {'status': False}
        for item in order:
            meal = Meal.query.filter_by(id=item.meal_id).first()
            user_order_data = {
                "id": item.id,
                "meal_id": item.meal_id,
                "user_id": item.customer_id,
                "meal_name": meal.meal_name,
                "price": meal.price
            }
            user_order_items.append(user_order_data)
            total += item.meal.price
        return {
            'status': True,
            "order_items": user_order_items,
            "total": total
        }
