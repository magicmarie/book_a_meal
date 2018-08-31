"""control properties of the order object"""
from api import DB
from api.models.menu import Menu
from api.models.meal import Meal
from api.models.user import User


class Order(DB.Model):
    """ control properties of the order object"""
    __tablename__ = "orders"
    id = DB.Column(DB.Integer, primary_key=True)
    meal_id = DB.Column(DB.Integer, DB.ForeignKey("meals.id"))
    customer_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    quantity = DB.Column(DB.Integer)
    admin_id = DB.Column(DB.Integer)
    user = DB.relationship('User', backref='orders')
    meal = DB.relationship('Meal', backref=DB.backref(
        'orders', cascade='all, delete-orphan'))

    def __repr__(self):
        """defines the representation of an object"""
        return "id:{} meal_id:{} user_id:{} admin_id:{}".format(
            self.id,
            self.meal_id, self.customer_id, self.admin_id)  # pragma:no cover

    def add_order(self, user, menu_id, meal_id, quantity):
        order = Menu.query.filter_by(id=menu_id, meal_id=meal_id).first()
        if not order:
            return {"status": False}
        meal = Meal.query.filter_by(id=meal_id).first()
        self.meal_id = meal_id,
        self.customer_id = user['id'],
        self.admin_id = meal.user_id,
        self.quantity = quantity
        DB.session.add(self)
        DB.session.commit()
        user_order = {
            "id": self.id, "meal_id": self.meal_id,
            "customer_id": user['id'], "admin_id": meal.user_id,
            "quantity": quantity,
            'meal_name': meal.meal_name,
            'meal_price': meal.price,
        }
        return {'status': True, "order": user_order}

    def find_order(self, order_id, user):
        order = Order.query.filter_by(id=order_id,
                                      customer_id=user['id']).first()
        if not order:
            return {"status": False,
                    "message": "Order not found"}
        return {"status": True, "order": order}

    def get_admin_orders(self, user, limit, page):
        if limit and page:
            try:
                limit = int(limit)
                page = int(page)
            except ValueError:
                status = False
                return {
                    "status": status,
                    'message': 'limit and page query parameters should be\
                    integers'
                }
        orderz = self.query.filter_by(admin_id=user['id']).order_by(
            Order.id.desc()).paginate(
            page=page, per_page=limit,
            error_out=False
        )
        return self.manipulate_orders(orderz)

    def get_user_orders(self, user, limit, page):
        if limit and page:
            try:
                limit = int(limit)
                page = int(page)
            except ValueError:
                status = False
                return {
                    "status": status,
                    'message': 'limit and page query parameters should be\
                    integers'
                }
        orders = self.query.filter_by(customer_id=user['id']).order_by(
            Order.id.desc()).paginate(page=page, per_page=limit,
                                      error_out=False)
        return self.manipulate_orders(orders)

    def manipulate_orders(self, orders):
        total_items = orders.total
        total_pages = orders.pages
        current_page = orders.page
        items_per_page = orders.per_page
        prev_page = None
        next_page = ''

        if orders.has_prev:
            prev_page = orders.prev_num
        if orders.has_next:
            next_page = orders.next_num

        orders = orders.items
        user_order_items = []
        total = 0
        for item in orders:
            meal = Meal.query.filter_by(id=item.meal_id).first()
            admin = User.query.filter_by(id=item.admin_id).first()
            customer = User.query.filter_by(id=item.customer_id).first()
            user_order_data = {
                "id": item.id,
                "meal_id": item.meal_id,
                "user_id": item.customer_id,
                "meal_name": meal.meal_name,
                "adminName": admin.name,
                "customerName": customer.name,
                "admin_id": meal.user_id,
                "price": meal.price,
                "quantity": item.quantity
            }
            user_order_items.append(user_order_data)
            total += item.meal.price

        responseObject = {
            'status': 'sucess',
            'next_page': next_page,
            'previous_page': prev_page,
            'total_count': total_items,
            'pages': total_pages,
            'current_page': current_page,
            'per_page': items_per_page,
            'orders': user_order_items,
            'total': total
        }
        return responseObject
