from app.models.meal import Meal


class Menu(object):
    menus = [
        {
            "day": "Monday",
            "menu":
            [
                {"Beef and rice",
                 "10000"}
                {
                    "Chips and chicken", "15000"}
            ]

        }
    ]

    def save(self, day, meals):
        self.menus.append({"day": Monday, "menu": menus})
