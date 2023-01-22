from xml.dom.minidom import Document
from pybars import Compiler
from weasyprint import HTML
import codecs
import locale

class InvoicePrinter:

    def __init__(self, Invoice, file_name):
        self.print_invoice(Invoice, file_name)

    def print_invoice(self, Invoice, pdf_filename):
        document_data = {}
        document_data['items'] = []
        document_data['totals'] = {
            'net' : 0,
            'gross': 0,
            'tax': 0,
        }
        document_data['from'] = Invoice.document_data['from']
        document_data['to'] = Invoice.document_data['to']
        document_data['currency'] = Invoice.currency
        document_data['invoice'] = {'invoice_number': Invoice.invoice_number, 'credit_number': Invoice.credit_number, 'customer_number': Invoice.customer_number, 'date': Invoice.today_date.strftime('%d.%m.%Y'), 'pay_until_date': Invoice.pay_until_date.strftime('%d.%m.%Y')}

        index = 1
        for item in Invoice.get_items():
            element = ({
                'index': index,
                'name': item.get_description(),
                'amount': item.get_amount(),
                'net_price': locale.format_string('%.2f', item.get_price()),
                'tax_rate': item.get_tax(),
                'total_net_price': locale.format_string('%.2f',item.get_total_price_net())
            })
            
            document_data['items'].append(element)
            document_data['totals']['net'] += item.get_total_price_net()
            document_data['totals']['gross'] += item.get_total_price()
            document_data['totals']['tax'] += item.get_total_price() - item.get_total_price_net()
            index += 1

        document_data['totals']['net'] = locale.format_string('%.2f', document_data['totals']['net'])
        document_data['totals']['gross'] = locale.format_string('%.2f', document_data['totals']['gross'])
        document_data['totals']['tax'] = locale.format_string('%.2f', document_data['totals']['tax'])
        self.output_pdf(Invoice.template, document_data, pdf_filename)

    def output_pdf(self, template, document_data, pdf_filename):
        with codecs.open(template, encoding="utf-8") as index_file:
            html_text = index_file.read()
            compiler = Compiler()
            template = compiler.compile(html_text)
            html_text = template(document_data)

            weasytemplate = HTML(string=html_text, base_url="template/invoice.html")
            weasytemplate.write_pdf(pdf_filename)