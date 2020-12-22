import codecs
import locale
from datetime import timedelta, date
from pybars import Compiler
from weasyprint import HTML

class Invoice:
    items = []
    template = ""
    document_data = {}

    tax_rate = 0
    currency = ''

    def __init__(self, template, invoice_number, invoice_from, invoice_to, tax_rate=19, currency='€', days_to_pay=14):
        today = date.today()
        pay_until_date = today + timedelta(days_to_pay)
        self.template = template
        self.document_data['invoice'] = {'invoice_number': invoice_number, 'customer_number':invoice_to['customer_number'], 'number': invoice_number, 'date': today.strftime('%d.%m.%Y'), 'pay_until_date': pay_until_date.strftime('%d.%m.%Y')}
        self.document_data['from'] = invoice_from
        self.document_data['to'] = invoice_to
        self.tax_rate = tax_rate
        self.currency = currency

    def add_item(self, item):
        self.items.append(item)

    def output_pdf(self, pdf_name):
        with codecs.open(self.template, encoding="utf-8") as index_file:
            html_text = index_file.read()

            self.document_data['totals'] = {
                'netto' : 0,
                'brutto': 0,
                'tax': 0,
            }
            self.document_data['items'] = self.items

            index = 1
            for item in self.document_data['items']:
                item['index'] = index
                item['total_netto_price'] = (item['netto_price'] * item['amount'])
                item['total_tax'] = (item['total_netto_price'] * (item['tax_rate'] / float(100)))
                item['total_brutto_price'] = (item['total_netto_price'] + item['total_tax'])

                self.document_data['totals']['netto'] += item['total_netto_price']
                self.document_data['totals']['brutto'] += item['total_brutto_price']
                self.document_data['totals']['tax'] += item['total_tax']

                item['tax_rate'] = locale.format("%.2f", item['tax_rate'])
                item['netto_price'] = locale.format("%.2f", item['netto_price'])
                item['total_netto_price'] = locale.format("%.2f", item['total_netto_price'])
                index += 1

            self.document_data['totals']['netto'] = locale.format("%.2f", self.document_data['totals']['netto'])
            self.document_data['totals']['brutto'] = locale.format("%.2f", self.document_data['totals']['brutto'])
            self.document_data['totals']['tax'] = locale.format("%.2f", self.document_data['totals']['tax'])
            
            compiler = Compiler()
            template = compiler.compile(html_text)
            html_text = template(self.document_data)

            #print(self.document_data)
            weasytemplate = HTML(string=html_text, base_url="template/index.html")
            weasytemplate.write_pdf(pdf_name)