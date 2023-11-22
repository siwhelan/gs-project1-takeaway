from lib.menu import Menu


# test to make sure display returns the list of dishes & prices
def test_display_menu_returns_menu_items():
    menu = Menu()
    assert "Chicken Wrap: 4.99" in menu.display_menu()
    assert "Fish and Chips: 10.99" in menu.display_menu()
