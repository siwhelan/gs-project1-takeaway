import os
import datetime
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(twilio_account_sid, twilio_auth_token)


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
        if not self.order:
            raise Exception(f"No order placed!")
        # calculates the total price of the order
        # returns total price
        return sum(quantity * price for item, quantity, price in self.order)

    def generate_receipt(self):
        if not self.order:
            raise Exception(f"No order placed!")
        # returns a receipt containing all items ordered,
        # individual prices and a total price
        receipt_lines = [
            f"{item} x{quantity}: {quantity * price:.2f}"
            for item, quantity, price in self.order
        ]
        total = self.calculate_total()
        receipt_lines.append(f"Total: {total:.2f}")
        return "\n".join(receipt_lines)

    def estimate_delivery_time(self):
        # returns a delivery time for the order based on 40 minutes from 'now'
        current_time = datetime.datetime.now()
        delivery_time = current_time + datetime.timedelta(minutes=40)
        return delivery_time

    def complete_order(self, number_to, number_from):
        if not self.order:
            raise Exception(f"No order placed!")
        self.completed = True
        delivery_time = self.estimate_delivery_time()
        order_receipt = self.generate_receipt()
        # Construct text
        confirmation_message = f"Your order has been placed and will be delivered by {delivery_time.strftime('%H:%M')}. Here is your receipt:\n{order_receipt}"
        # Send text
        self.generate_confirmation_text(number_to, number_from, confirmation_message)

    def generate_confirmation_text(self, number_to, number_from, message):
        # Send the message
        message = client.messages.create(to=number_to, from_=number_from, body=message)
        return message.sid
