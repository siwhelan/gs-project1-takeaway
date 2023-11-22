from lib.menu import Menu
from lib.order import Order
import pytest


# test add_items correctly adds single item and quantity to the order
def test_adding_item_from_menu_to_order():
    menu = Menu()
    order = Order()
    dish_name = "Chicken Wrap"
    quantity = 2
    # Add the dish to the order from the menu
    order.add_items(menu, dish_name, quantity)
    # Check if the order contains the item with the correct quantity and price
    expected_item = (dish_name, quantity, menu.dishes[dish_name])
    assert expected_item in order.order


# test adding multiple items
def test_adding_item_from_menu_to_order():
    menu = Menu()
    order = Order()

    # Add items to the order
    order.add_items(menu, "Chicken Wrap", 1)
    order.add_items(menu, "Large Fries", 1)
    order.add_items(menu, "Soft Drink", 2)

    # Expected items in the order
    # menu.dishes[item] is used to obtain the price
    expected_items = [
        ("Chicken Wrap", 1, menu.dishes["Chicken Wrap"]),
        ("Large Fries", 1, menu.dishes["Large Fries"]),
        ("Soft Drink", 2, menu.dishes["Soft Drink"]),
    ]

    assert order.order == expected_items


# test add_items raises an error if the item is not available
def test_add_items_raises_an_error_if_the_item_is_not_available():
    menu = Menu()
    order = Order()
    dish_name = "Kebab Wrap"  # An item not in the menu
    quantity = 1

    with pytest.raises(ValueError) as err:
        order.add_items(menu, dish_name, quantity)

    assert str(err.value) == "Kebab Wrap is not available!"


# test grand total generation when adding multiple items to an order
def test_order_total_with_menu_integration():
    menu = Menu()
    order = Order()

    # Add items to the order using the menu
    order.add_items(menu, "Chicken Wrap", 2)
    order.add_items(menu, "Large Fries", 1)

    # Calculate expected total
    expected_total = menu.dishes["Chicken Wrap"] * 2 + menu.dishes["Large Fries"] * 1

    # Assert that the calculated total is as expected
    assert order.calculate_total() == expected_total
