from lib.order import Order


# Initializes with an empty order list
def test_order_is_initially_empty():
    new_order = Order()
    assert new_order.order == []


# test 'completed' is initially false
def test_completed_is_initially_false():
    order = Order()
    assert order.completed == False


# test complete_order marks the order as complete
def test_mark_as_complete():
    order = Order()
    order.complete_order()
    assert order.completed == True


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
