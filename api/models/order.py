"""control properties of the order object"""
from api import DB
from api.models.menu import Menu


class Order(DB.Model):
    """ control properties of the order object"""
    __tablename__ = "orders"
    id = DB.Column(DB.Integer, primary_key=True)
    meal_id = DB.Column(DB.Integer, DB.ForeignKey("meals.id"))
    user_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    admin_id = DB.Column(DB.Integer)
    user = DB.relationship('User', backref='orders')
    meal = DB.relationship('Meal', backref='orders')

    def __repr__(self):
        """defines the representation of an object"""
        return "id:{} meal_id:{} user_id:{}".format(
            self.orderId, self.meal_id, self.user_id)  # pragma:no cover

    def add_order(self, res, meal_id):
        order = Menu.query.filter_by(meal_id=meal_id).first()
        if not order:
            return {"status": False}
        new_order = self(
            meal_id=meal_id,
            user_id=res['decoded']['id'],
            admin_id=order.meal.user_id)
        DB.session.add(new_order)
        DB.session.commit()
        return {'status': True}

    def get_admin_orders(self, res):
        total = 0
        orderz = self.query.filter_by(admin_id=res['decoded']['id']).all()
        if orderz:
            order_items = []
            for order in orderz:
                order_data = {
                    "id": order.id,
                    "meal_id": order.meal_id,
                    "user_id": order.user_id,
                    "meal_name": order.meal_name,
                    "price": order.price,
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
        order = self.query.filter_by(user_id=res['decoded']['id']).all()
        user_order_items = []
        total = 0
        if not order:
            return {'status': False}
        for item in order:
            user_order_data = {
                "id": item.id,
                "meal_id": item.meal_id,
                "user_id": item.user_id
            }
            user_order_items.append(user_order_data)
            total += order.meal.price
            return {
                'status': True,
                "order_items": user_order_items,
                "total": total
            }
