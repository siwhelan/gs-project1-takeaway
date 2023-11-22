class Order:
    def __init__(self):
        # initialises customer order list
        # completed = false
        self.order = []
        self.completed = False

    def add_items(self, menu, item_name, quantity):
        # Check if the item is in the menu
        if item_name not in menu.dishes:
            raise ValueError(f"{item_name} is not available!")

        else:
            price = menu.dishes[item_name]
            self.order.append((item_name, quantity, price))

    def calculate_total(self):
        # calculates the total price of the order
        # returns total price
        return sum(quantity * price for item, quantity, price in self.order)

    def generate_receipt():
        # returns a receipt containing all items ordered,
        # individual prices and a total price
        pass

    def estimate_delivery_time():
        # returns a delivery time for the order based on 40 minutes from 'now'
        pass

    def complete_order(self):
        # marks completed as true
        # sends customer a confirmation text & expected delivery time - TODO
        self.completed = True
