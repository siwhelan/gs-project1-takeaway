class Menu:
    def __init__(self):
        # initialises menu of dishes
        # which contains a dict of dishes e.g [name, price]
        self.dishes = {
            "Cheeseburger": 8.99,
            "Chicken Nuggets": 5.49,
            "Veggie Burger": 6.79,
            "Fish and Chips": 10.99,
            "Hot Dog": 5.49,
            "Chicken Wrap": 4.99,
            "Large Fries": 1.99,
            "Soft Drink": 0.99,
            "Bottled Water": 0.79,
            "Milkshake": 2.99,
        }

    def display_menu(self):
        # returns a list of all menu items & their prices
        return [f"{item}: {price}" for item, price in self.dishes.items()]
