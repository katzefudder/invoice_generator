from lib.item import Item
import pytest

class TestItem:
    def test_invoice_arithmetics(self):
        item = Item('line item', 12, 2, 19)
        assert item.get_price() == 12.00
        assert item.get_total_price_net() == 24.00
        assert item.get_tax() == 19
        assert item.get_total_tax() == 4.56
        assert item.get_total_price() == 28.56

    def test_extended_invoice_arithmetics(self):
        item = Item('line item', 12.23, 2.5, 19)
        assert item.get_price() == 12.23
        assert item.get_total_price_net() == 30.575
        assert item.get_tax() == 19
        assert item.get_total_tax() == 5.81
        assert item.get_total_price() == 36.38

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

    def test_item_with_tax_lower_than_zero(self):
        with pytest.raises(Exception) as error:
            item = Item('line item', 10, 1, -1)
        assert "tax cannot be negative" in str(error.value)

    def test_item_with_floating_point_price(self):
        item = Item('line item', 12.0283734821, 7, 19)
        assert item.get_total_price_net() == 84.199
        assert item.get_total_tax() == 16.00
        assert item.get_total_price() == 100.20

    def test_set_amount(self):
        item = Item('line item', 12.0283734821, 7, 19)
        item.set_amount(12)
        assert item.get_amount() == 12

if __name__ == "__main__":
    test = TestItem()