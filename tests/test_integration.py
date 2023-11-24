from lib.menu import Menu
from lib.order import Order
from unittest import mock
from dotenv import load_dotenv
import pytest
import datetime
import os


load_dotenv()


# # test add_items correctly adds single item and quantity to the order
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
def test_adding_multiple_items_from_menu_to_order():
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


# test complete_order marks an order as complete
def test_mark_as_complete():
    order = Order()
    menu = Menu()
    order.add_items(menu, "Hot Dog", 5.49)
    with mock.patch("lib.order.client.messages.create") as mock_create:
        mock_create.return_value.sid = "MockedSID"
        order.complete_order("07979685746", "07968576857")
    assert order.completed == True


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


# test simple text generation with Twilio API
def test_generate_confirmation_text():
    with mock.patch("lib.order.client.messages.create") as mock_create:
        mock_create.return_value.sid = "MockedSID"
        order = Order()
        result = order.generate_confirmation_text(
            "<to_number>", "<from_number>", "message"
        )

        mock_create.assert_called_with(
            to="<to_number>", from_="<from_number>", body="message"
        )
        assert result == "MockedSID"


# fully test complete_order integration
def test_complete_order_integration():
    # Mocking internal methods of Order class
    with mock.patch(
        "lib.order.Order.estimate_delivery_time"
    ) as mock_estimate, mock.patch(
        "lib.order.Order.generate_receipt"
    ) as mock_receipt, mock.patch(
        "lib.order.Order.generate_confirmation_text"
    ) as mock_text:
        # Setting return values for the mocked methods
        mock_estimate.return_value = datetime.datetime(2023, 1, 1, 12, 0)
        mock_receipt.return_value = "Receipt details"

        # Setup: Creating order and adding items
        order = Order()
        menu = Menu()
        order.add_items(menu, "Chicken Wrap", 2)
        order.add_items(menu, "Large Fries", 1)

        # Testing complete_order method
        order.complete_order("mock_to_number", "mock_from_number")

        # Asserting that mocked methods were called correctly
        mock_estimate.assert_called_once()
        mock_receipt.assert_called_once()
        expected_message = "Your order has been placed and will be delivered by 12:00. Here is your receipt:\nReceipt details"
        mock_text.assert_called_once_with(
            "mock_to_number", "mock_from_number", expected_message
        )

        # Final assertion to check if the order is marked as completed
        assert order.completed == True


# Mock Twilio client creation
@pytest.mark.skip(reason="Disable actual texts during testing")
@mock.patch("lib.order.Client")
def test_twilio_integration(self, mock_client_class):
    # Create a mock Twilio client instance
    mock_twilio_client = mock_client_class.return_value
    mock_twilio_client.messages.create.return_value.sid = "MockedSID"

    order = Order()
    menu = Menu()
    order.add_items(menu, "Chicken Wrap", 2)
    order.add_items(menu, "Large Fries", 1)

    to_number = os.getenv("TWILIO_TO_NUMBER")
    from_number = os.getenv("TWILIO_FROM_NUMBER")

    result = order.complete_order(to_number, from_number)

    mock_twilio_client.messages.create.assert_called_with(
        to=to_number,
        from_=from_number,
        body=mock.ANY,  # You can check the exact message content here
    )

    assert result == "MockedSID"


"""
This test does the following:

Mocks the messages.create method of the Twilio client.
Creates instances of Menu and Order.
Adds a 'Cheeseburger' from the menu to the order.
Calls complete_order on the Order instance, which triggers a text message via Twilio.
Asserts that the mocked messages.create method was called with the expected arguments.
"""


@mock.patch(
    "lib.order.client.messages.create"
)  # Mock the Twilio messages.create method
def test_complete_order_sends_confirmation_text(mock_create):
    # Setup mock response for messages.create
    mock_create.return_value.sid = "mocked_sid"
    # Create an instance of Menu and Order
    test_menu = Menu()
    test_order = Order()
    # Add an item from the menu to the order
    test_order.add_items(test_menu, "Cheeseburger", 1)
    # Call complete_order which should trigger generate_confirmation_text
    test_order.complete_order("test_to_number", "test_from_number")
    # Assert that the Twilio messages.create method was called with expected arguments
    mock_create.assert_called_once_with(
        to="test_to_number",
        from_="test_from_number",
        body=mock.ANY,  # exact message content isn't important for this test, just a response
    )


# test different orders generate different messages
@mock.patch("lib.order.client.messages.create")
def test_twilio_message_content_for_different_orders(mock_create):
    test_menu = Menu()
    test_order = Order()
    test_order.add_items(test_menu, "Chicken Wrap", 2)
    test_order.complete_order("test_to_number", "test_from_number")
    message_body_1 = mock_create.call_args[1]["body"]

    test_order = Order()
    test_order.add_items(test_menu, "Bottled Water", 1)
    test_order.complete_order("test_to_number", "test_from_number")
    message_body_2 = mock_create.call_args[1]["body"]

    assert message_body_1 != message_body_2


# test twilio is not called on an empty order
@mock.patch("lib.order.client.messages.create")
def test_twilio_not_called_for_empty_order(mock_create):
    test_order = Order()
    with pytest.raises(Exception):
        test_order.complete_order("test_to_number", "test_from_number")
    mock_create.assert_not_called()
