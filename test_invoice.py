from lib.invoice import Invoice
from lib.item import Item
import pytest
import os

class TestInvoice:
    def test_simple_invoice(self):
        invoice = Invoice("invoices/test.yaml")
        invoice.add_item(Item('dummy item', 2.54, 3, 20))
        data = invoice.get_document_data()
        assert data['from']['name'] == 'John Doe'
        assert data['from']['street'] == 'Random Street'
        assert data['from']['city'] == 'Random Town'
        assert data['from']['postcode'] == 4711

        assert data['to']['name'] == 'Jane Doe'
        assert data['to']['street'] == 'Random Other Street'
        assert data['to']['city'] == 'Random Other Town'
        assert data['to']['postcode'] == 4711815

        items = invoice.get_items()
        assert items[0].get_description() == 'dummy item'
        assert items[0].get_price() == 2.54
        assert items[0].get_tax() == 20
        assert items[0].total_price == 9.144
        assert items[0].get_total_price() == 9.14 # rounded value
        assert items[0].total_price_net == 7.62
        assert items[0].get_total_price_net() == 7.62
        assert items[0].get_total_tax() == 1.524

        invoice.output_pdf('test.pdf')
        assert os.path.exists('test.pdf')

