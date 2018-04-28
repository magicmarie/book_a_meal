class Meal(object):
    meals = [{
        "name": "Matooke with g-nuts",
        "price": "10000",
    }
    ]

    def save(self, meal):
        self.meals.append(meal)

    def get_meals(self):
        return self.meals
