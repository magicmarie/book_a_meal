"""control properties of the meal object"""
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
            self.id,
            self.meal_name,
            self.price,
            self.user_id)  # pragma:no cover

    def validate_inputs(self):
        """function to validate meal details"""
        status = True
        messages = []
        meal_name = self.meal_name.strip()
        if meal_name == "" or len(meal_name) < 3 or len(meal_name) > 25:
            status = False
            messages.append(
                "Meal name must be between 3 to 25 characters long")
        if not bool(re.fullmatch('^[A-Za-z ]*$', meal_name)):
            status = False
            messages.append("Invalid characters not allowed")
        if self.price <= "0":
            status = False
            messages.append("Price must be a positive number")
        try:
            int(self.price)
        except ValueError:
            status = False
            messages.append("Price must be a number")
        return {"status": status, "message": ", ".join(messages)}

    @classmethod
    def get_meals(cls, user, limit, page):
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
        meals = cls.query.filter_by(
            user_id=user['id']).order_by(Meal.id.desc()).paginate(
            page=page, per_page=limit,
            error_out=False
        )
        return meals

    @staticmethod
    def meals_serializer(meals):
        total_items = meals.total
        total_pages = meals.pages
        current_page = meals.page
        items_per_page = meals.per_page
        prev_page = None
        next_page = ''

        if meals.has_prev:
            prev_page = meals.prev_num
        if meals.has_next:
            next_page = meals.next_num

        meals = meals.items

        meals_list = []
        for meal in meals:
            meal_data = {}
            meal_data['id'] = meal.id
            meal_data['user_id'] = meal.user_id
            meal_data['name'] = meal.meal_name
            meal_data['price'] = meal.price
            meals_list.append(meal_data)

        responseObject = {
            'status': 'sucess',
            'nextPage': next_page,
            'previousPage': prev_page,
            'totalCount': total_items,
            'pages': total_pages,
            'currentPage': current_page,
            'perPage': items_per_page,
            'meals': meals_list
        }
        return responseObject

    def save_meal(self, meal_name, price, user):
        meal = self.query.filter_by(
            meal_name=meal_name,
            user_id=user['id']).first()
        if meal:
            return {"status": False}
        self.meal_name = meal_name
        self.price = price
        self.user_id = user['id']
        DB.session.add(self)
        DB. session.commit()
        return {"status": True, "id": self.id,
                "meal_name": self.meal_name, "price": self.price}

    @classmethod
    def find_meal(cls, meal_id, user):
        meal = Meal.query.filter_by(
            user_id=user['id'],
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

    def delete_meal(self):
        DB.session.delete(self)
        DB.session.commit()
