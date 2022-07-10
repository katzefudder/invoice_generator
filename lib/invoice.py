import codecs
from lib.aws_item import AwsItem
from lib.item import Item
import locale
import yaml
from datetime import timedelta, date
from pybars import Compiler
from weasyprint import HTML

class Invoice:
    items = []
    template = "template/invoice.html"
    document_data = {}

    tax_rate = 0
    currency = '€'

    def __init__(self, invoice_yaml, currency='€', days_to_pay=14, fromDate='', toDate='', template='', overrideInvoiceDate='', overrideInvoiceNumber='', overrideTax='', creditNumber=''):
        with open(invoice_yaml, 'r') as yaml_in:
            data = yaml.load(yaml_in, Loader=yaml.FullLoader)

        # collect items from invoices folder yaml
        for key, element in data['items'].items():
            if overrideTax == '':
                tax = element['tax']
            else:
                tax = int(overrideTax)

            if element['type'] == 'aws_item':
                self.add_item(AwsItem(element['profile'], element['description'], element['tag'], fromDate, toDate, tax))
            else:
                self.add_item(Item(element['description'], element['price'], element['amount'], tax))

        if overrideInvoiceDate == '':
            today = date.today()
        else:
            today = date.fromisoformat(overrideInvoiceDate)

        pay_until_date = today + timedelta(days_to_pay)

        if overrideInvoiceNumber == '':
            invoiceNumber = data['from']['invoice_number']
        else:
            invoiceNumber = overrideInvoiceNumber

        self.document_data['invoice'] = {'invoice_number': invoiceNumber, 'credit_number': creditNumber, 'customer_number':data['to']['customer_number'], 'date': today.strftime('%d.%m.%Y'), 'pay_until_date': pay_until_date.strftime('%d.%m.%Y')}
        self.document_data['from'] = data['from']
        self.document_data['to'] = data['to']
        self.currency = currency

        self.template = template

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

    def prepare_invoice_items(self):
        self.document_data['currency'] = self.currency
        self.document_data['totals'] = {
            'net' : 0,
            'gross': 0,
            'tax': 0,
        }
        self.document_data['items'] = []

        index = 1
        for item in self.items:
            element = ({
                'index': index,
                'name': item.get_description(),
                'amount': item.get_amount(),
                'net_price': locale.format_string('%.2f', item.get_price()),
                'tax_rate': item.get_tax(),
                'total_net_price': locale.format_string('%.2f',item.get_total_price_net())
            })
            
            self.document_data['items'].append(element)
            self.document_data['totals']['net'] += item.get_total_price_net()
            self.document_data['totals']['gross'] += item.get_total_price()
            self.document_data['totals']['tax'] += item.get_total_price() - item.get_total_price_net()
            index += 1

        self.document_data['totals']['net'] = locale.format_string('%.2f', self.document_data['totals']['net'])
        self.document_data['totals']['gross'] = locale.format_string('%.2f', self.document_data['totals']['gross'])
        self.document_data['totals']['tax'] = locale.format_string('%.2f', self.document_data['totals']['tax'])

    def output_pdf(self, pdf_name):
        self.prepare_invoice_items()
        with codecs.open(self.template, encoding="utf-8") as index_file:
            html_text = index_file.read()
            compiler = Compiler()
            template = compiler.compile(html_text)
            html_text = template(self.document_data)

            weasytemplate = HTML(string=html_text, base_url="template/invoice.html")
            weasytemplate.write_pdf(pdf_name)