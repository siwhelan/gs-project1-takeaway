```markdown
# Golden Square Project 1 - Takeaway
 
 ## 1. Describe the Problem
 
    As a customer
    So that I can check if I want to order something
    I would like to see a list of dishes with prices.

    As a customer
    So that I can order the meal I want
    I would like to be able to select some number of several available dishes.

    As a customer
    So that I can verify that my order is correct
    I would like to see an itemised receipt with a grand total.

    As a customer
    So that I am reassured that my order will be delivered on time
    I would like to receive a text such as "Thank you! Your order was placed and will be delivered before 18:52" after I have ordered.


 ## 2. Design the Class System
 
```python


class Menu():

    def __init__(self):
        # initialises menu of dishes
        # which contains a list dishes e.g [name, price]
        pass

    def display_menu():
        # returns a list of all menu items & their prices
        pass
```
---

```python


class Order:
    def __init__():
        # initialises customer order list
        # completed = false
        pass

    def add_items():
        # adds items to order list
        # with prices
        # returns nothing
        pass

    def calculate_total():
        # calculates the total price of the order
        # returns total price
        pass

    def generate_receipt():
        # returns a receipt containing all items ordered,
        # individual prices and a total price
        pass

    def estimate_delivery_time():
        # returns a delivery time for the order based on 40 minutes from 'now'
        pass

    def complete_order():
        # marks completed as true
        # sends customer a confirmation text & expected delivery time
        pass

```
 
 ## 3. Create Examples as Unit Tests
 
```python

# Menu Class
# test to make sure display returns the list of dishes & prices
menu = Menu() 
# => 'Dish Name - Price' in menu.display()

# Order Class
# Initializes with an empty order list/dict (TBC)
order = Order()

# Test to ensure items and quantities can be added to the order
# => 'Dish Name - Quantity' in order.items after order.add_item('Dish Name', quantity)

# Test to ensure the total is calculated correctly
# => order.calculate_total() == expected_total

# Test to ensure an itemised receipt with each dish, its quantity, price, and a grand total is generated
# => 'Dish Name - Quantity - Price\nGrand Total: Total Amount' in order.generate_receipt()


# complete order - TODO

 
``` 
 ## 4. Create Examples as Integration Tests
 
```python
# Test Order Interaction with Menu
```
- Create `Menu` and `Order` instances.
- Add 'Pizza' to menu with price 9.99.
- Add 2 'Pizza' to order.
- Calculate total, expect 19.98.
- Generate receipt, confirm 'Pizza' and '19.98' present.
