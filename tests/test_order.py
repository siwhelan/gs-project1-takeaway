from lib.order import Order
from lib.menu import Menu
from unittest import mock
import datetime
import pytest


# Initializes with an empty order list
def test_order_is_initially_empty():
    new_order = Order()
    assert new_order.order == []


# test 'completed' is initially false
def test_completed_is_initially_false():
    order = Order()
    assert order.completed == False


# test an empty order beuing completed raises an error
def test_error_raised_when_empty_order_is_completed():
    order = Order()
    order.order = []
    with pytest.raises(Exception) as err:
        order.generate_receipt()
    assert str(err.value) == "No order placed!"


# Test to ensure the total is calculated correctly
# => order.calculate_total() == expected_total
def test_single_item_order_total_is_calculated_correctly():
    order = Order()
    order.order = [
        ("Item1", 2, 5.00),  # 2 items at 5.00 each
        ("Item2", 1, 3.50),  # 1 item at 3.50
    ]
    expected_total = 13.50
    assert order.calculate_total() == expected_total


# test generate_receipt raises an error if there is no order
def test_error_raised_when_total_is_calculated_on_empty_order():
    order = Order()
    order.order = []
    with pytest.raises(Exception) as err:
        order.generate_receipt()
    assert str(err.value) == "No order placed!"


# test generate_receipt raises an error if there is no order
def test_error_raised_when_receipt_is_generated_on_empty_order():
    order = Order()
    order.order = []
    with pytest.raises(Exception) as err:
        order.generate_receipt()
    assert str(err.value) == "No order placed!"


# Test to ensure an itemised receipt with each dish, its quantity,
# price, and a grand total is generated
def test_receipt_generation():
    order = Order()
    order.order = [("Item1", 2, 5.00)]  # 2 items at 5.00 each
    # expected_total = 10
    assert order.generate_receipt() == f"Item1 x2: 10.00\nTotal: 10.00"


# test multiple item order receipt
def test_multiple_item_order_receipt():
    order = Order()
    order.order = [("Item1", 2, 5.00), ("Item2", 3, 3.00), ("Item3", 1, 2.00)]
    assert (
        order.generate_receipt()
        == f"Item1 x2: 10.00\nItem2 x3: 9.00\nItem3 x1: 2.00\nTotal: 21.00"
    )


# test creation of delivery time estimate - 40 minutes from 'now'
def test_estimate_delivery_time():
    order = Order()
    # assign a fake time
    mocked_current_time = datetime.datetime(2023, 11, 23, 12, 0)
    # patch the behaviour of datetime with our fake one
    with mock.patch("datetime.datetime") as mocked_datetime:
        mocked_datetime.now.return_value = mocked_current_time
        # assign the expected delivery time to = 40 minutes from our 'fake' time
        expected_delivery_time = mocked_current_time + datetime.timedelta(minutes=40)
        # assert that delivery time is 40 mins from 'now'
        assert order.estimate_delivery_time() == expected_delivery_time
