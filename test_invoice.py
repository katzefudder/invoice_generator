from argparse import FileType
from operator import inv
from unicodedata import name

from lib.invoice import Invoice
from lib.item import Item
import pytest
import os
import io

def test_simple_invoice(mocker):
    mocker.patch('lib.aws_item.AwsItem.get_costs_and_usage_from_aws', return_value=None)
    
    filename = "/tmp/test.pdf"
    output = open(file=filename, mode='w')

    invoice = Invoice(data="invoices/test.yaml", output=output)
    invoice.set_template('template/invoice.html')
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
    assert len(items) == 3
    
    first_item = items[0]
    assert first_item.get_description() == 'Ein Sack Reis'
    assert first_item.get_price() == 2.54
    assert first_item.get_tax() == 20
    assert first_item.total_price == 9.144
    assert first_item.get_total_price() == 9.14 # rounded value
    assert first_item.total_price_net == 7.62
    assert first_item.get_total_price_net() == 7.62
    assert first_item.get_total_tax() == 1.52

    second_item = items[1]
    assert second_item.get_description() == 'Zwei Dosen Luft'
    assert second_item.get_price() == 3.98
    assert second_item.get_tax() == 20
    assert second_item.total_price == 9.552
    assert second_item.get_total_price() == 9.55 # rounded value
    assert second_item.total_price_net == 7.96
    assert second_item.get_total_price_net() == 7.96
    assert second_item.get_total_tax() == 1.59

    third_item = items[2]
    assert third_item.get_description() == 'S3 und AWS CloudFront (01.01.2021 - 31.01.2021)'
    assert third_item.get_price() == 0.00
    assert third_item.get_tax() == 19
    assert third_item.get_total_price() == 0.00
    assert third_item.total_price_net == 0.00
    assert third_item.get_total_tax() == 0.00

    assert invoice.document_data['totals']['tax'] == "3.11"
    assert invoice.document_data['totals']['gross'] == "18.69"
    assert invoice.document_data['totals']['net'] == "15.58"

    #assert os.path.exists('test.pdf')

def test_crooked_yaml(mocker):
    mocker.patch('lib.aws_item.AwsItem.get_costs_and_usage_from_aws', return_value=None)

    invoice = Invoice(data="invoices/not_available.yaml")
    with pytest.raises(IOError) as excinfo:   
        invoice.process_invoice_document()
    
    invoice.set_template('template/invoice.html')
    data = invoice.get_document_data()
