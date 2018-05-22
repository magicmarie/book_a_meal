from api import DB


class User(DB.Model):
    __tablename__ = "users"
    id = DB.Column(DB.Integer, primary_key=True)
    userId = DB.Column(DB.Integer, unique=True)
    name = DB.Column(DB.String(50))
    email = DB.Column(DB.String, unique=True)
    password = DB.Column(DB.String)
    isAdmin = DB.Column(DB.Boolean, default=False)
    orders = DB.relationship('Order', backref='users')
    meals = DB.relationship('Meal', backref='users')

    def __repr__(self):
        return "userId:{} name:{} email:{} isAdmin:{} orders:{}".format(self.userId, self.name, self.email, self.isAdmin, self.orders)


class Order(DB.Model):
    __tablename__ = "orders"
    id = DB.Column(DB.Integer, primary_key=True)
    orderId = DB.Column(DB.Integer, unique=True)
    mealId = DB.Column(DB.String(50))
    userId = DB.Column(DB.Integer, DB.ForeignKey("users.userId"))
    menuName = DB.Column(DB.String(50), DB.ForeignKey("menus.menuName"))

    def __repr__(self):
        return "orderId:{} mealId:{} userId:{}".format(self.orderId, self.mealId, self.userId)


class Meal(DB.Model):
    __tablename__ = "meals"
    id = DB.Column(DB.Integer, primary_key=True)
    mealId = DB.Column(DB.Integer, unique=True)
    mealName = DB.Column(DB.String(50), unique=True)
    price = DB.Column(DB.Integer)
    userId = DB.Column(DB.Integer, DB.ForeignKey("users.userId"))
    menus = DB.relationship('Menu', backref='meals')

    def __repr__(self):
        return "mealId:{} mealName:{} price:{} userId:{} menus:{}".format(self.mealId, self.mealName, self.price, self.userId, self.menus)


class Menu(DB.Model):
    __tablename__ = "menus"
    id = DB.Column(DB.Integer, primary_key=True)
    menuId = DB.Column(DB.Integer, unique=True)
    menuName = DB.Column(DB.String(50))
    mealId = DB.Column(DB.Integer, DB.ForeignKey("meals.mealId"))
    orders = DB.relationship('Order', backref='menus')

    def __repr__(self):
        return "menuId:{} menuName:{} mealId:{} orders:{}".format(self.menuId, self.menuName, self.mealId, self.orders)


DB.create_all()
