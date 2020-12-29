from lib.item import Item
import pytest

class TestItem:
    def test_invoice_arithmetics(self):
        item = Item('line item', 12, 2, 19)
        assert item.get_price() == 12.00
        assert item.get_total_price_net() == 24.00
        assert item.get_total_price() == 28.56

    def test_item_with_no_tax(self):
        item = Item('line item', 12, 2, 0)
        assert item.get_total_price_net() == 24.00
        assert item.get_total_price() == 24.00

    def test_item_with_price_lower_than_zero(self):
        with pytest.raises(Exception) as error:
            item = Item('line item', -10, 10, 0)
        assert "price cannot be negative" in str(error.value)

    def test_item_with_amount_lower_than_zero(self):
        with pytest.raises(Exception) as error:
            item = Item('line item', 10, -10, 0)
        assert "amount cannot be negative" in str(error.value)

    def test_item_with_floating_point_price(self):
        item = Item('line item', 12.0283734821, 7, 19)
        assert item.get_total_price_net() == 84.2

    def test_set_amount(self):
        item = Item('line item', 12.0283734821, 7, 19)
        amount = 12
        item.set_amount(amount)
        assert item.get_amount() == amount

if __name__ == "__main__":
    test = TestItem()