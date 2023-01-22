from lib.aws_item import AwsItem
from lib.item import Item
from lib.invoice_printer import InvoicePrinter
import yaml
from datetime import timedelta, date
from pybars import Compiler
from weasyprint import HTML

class Invoice:
    items = []
    template = "template/invoice.html"
    document_data = {}

    invoice_number = ''
    credit_number = ''
    customer_number = ''
    
    today_date = ''
    from_date = ''
    to_date = ''

    tax_rate = 0
    currency = '€'

    def __init__(self, data, output, currency='€', days_to_pay=14, template='template/invoice.html', overrideInvoiceDate='', overrideInvoiceNumber='', overrideTax='', creditNumber=''):
        self.process_invoice_document(data, overrideTax, overrideInvoiceNumber)

        self.template = template
        self.currency = currency

        if overrideInvoiceDate == '':
            self.today_date = date.today()
        else:
            self.today_date = date.fromisoformat(overrideInvoiceDate)

        self.pay_until_date = self.today_date + timedelta(days_to_pay)

        self.document_data['invoice'] = {'invoice_number': self.invoice_number, 'credit_number': creditNumber, 'customer_number':self.customer_number, 'date': self.today_date.strftime('%d.%m.%Y'), 'pay_until_date': self.pay_until_date.strftime('%d.%m.%Y')}

        InvoicePrinter(self, output.name)

    def process_invoice_document(self, data, overrideTax, overrideInvoiceNumber):
        with open(data, 'r') as yaml_in:
            try:
                data = yaml.load(yaml_in, Loader=yaml.FullLoader)
            except yaml.YAMLError as yamlException:
                # TODO: test for broken yaml
                raise yamlException

        self.document_data['currency'] = self.currency
        self.document_data['totals'] = {
            'net' : 0,
            'gross': 0,
            'tax': 0,
        }
        self.document_data['items'] = []
        self.customer_number = data['to']['customer_number']
        self.document_data['from'] = data['from']
        self.document_data['to'] = data['to']
        self.document_data['from_date'] = data['from_date']
        self.document_data['to_date'] = data['to_date']

        if overrideInvoiceNumber == '':
            self.invoice_number = data['from']['invoice_number']
        else:
            self.invoice_number = overrideInvoiceNumber

        # collect items from invoices folder yaml
        for key, element in data['items'].items():
            if overrideTax == '':
                tax = element['tax']
            else:
                tax = int(overrideTax)

            if element['type'] == 'aws_item':
                self.add_item(AwsItem(element['profile'], element['description'], element['tag'], self.document_data['from_date'], self.document_data['to_date'], tax))
            else:
                self.add_item(Item(element['description'], element['price'], element['amount'], tax))

    def add_item(self, item: Item):
        self.items.append(item)

    def set_template(self, template):
        self.template = template

    def get_template(self):
        return self.template

    def get_item(self, position:int):
        return self.items[position]

    def get_items(self):
        return self.items

    def get_document_data(self):
        return self.document_data