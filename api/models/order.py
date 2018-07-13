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

    def add_order(self, user, menu_id, meal_id):
        order = Menu.query.filter_by(id=menu_id, meal_id=meal_id).first()
        if not order:
            return {"status": False}
        meal = Meal.query.filter_by(id=meal_id).first()
        self.meal_id = meal_id,
        self.customer_id = user['id'],
        self.admin_id = meal.user_id
        DB.session.add(self)
        DB.session.commit()
        return {'status': True}

    def get_admin_orders(self, user):
        orderz = self.query.filter_by(admin_id=user['id']).all()
        return self.manipulate_orders(orderz)

    def get_user_orders(self, user):
        orders = self.query.filter_by(customer_id=user['id']).all()
        return self.manipulate_orders(orders)

    def manipulate_orders(self, orders):
        user_order_items = []
        total = 0
        for item in orders:
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
