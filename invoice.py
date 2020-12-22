from lib.line_item import Line_item
import os
import boto3
import datetime
import argparse
import locale

from lib.invoice import Invoice

parser = argparse.ArgumentParser(description='Convert HTML template to pdf with data from yaml')
parser.add_argument('--template', help='The name of the template to use (e.g. invoice)', default="invoice.html")
parser.add_argument('--output_pdf', help='The output pdf file', default="pdf.pdf",  type=argparse.FileType('w'))
parser.add_argument('--locale', help='The locale to use', default="de_DE.UTF-8")

args = parser.parse_args()
locale.setlocale(locale.LC_ALL, args.locale)

client = boto3.client('ce', 'eu-central-1')

now = datetime.datetime.utcnow()

start = now.replace(day=1).strftime('%Y-%m-%d')
end = (datetime.date(now.year + now.month // 12, now.month % 12 + 1, 1) - datetime.timedelta(1)).strftime('%Y-%m-%d')

print ("%s -> %s" % (start, end))

results = []
customer = 'del2'

filterproject = {
    "Tags": {
        "Key": "Project",
        "Values": [
            customer,
        ]
    }
}

results = client.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, Granularity='MONTHLY', Metrics=['UnblendedCost'], Filter=filterproject)
costs = float(results['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])

invoice_number = '4711'
invoice_from = {'name': 'Florian Dehn', 'street': 'Feldbornstrasse 2', 'postcode': '35510', 'city': 'Butzbach'}
invoice_to = {'customer_number': '10001', 'name': 'König Drosselbart', 'street': 'Irgendwo 2', 'postcode': '08154711', 'city': 'Nirgendwo'}
template_file = 'template/' + args.template
invoice = Invoice(template=template_file, invoice_number=invoice_number, invoice_from=invoice_from, invoice_to=invoice_to)

invoice.add_item({'name': 'AWS CloudFront + S3 '+customer + " "+start+ " - "+end, 'amount': 1, 'netto_price': costs, 'tax_rate': 0})
invoice.add_item({'name': 'Ionos Hosting pixplace', 'amount': 1, 'netto_price': 20, 'tax_rate': 0})
invoice.add_item({'name': 'Servicepauschale + Wartung + Support', 'amount': 1, 'netto_price': 20, 'tax_rate': 0})
invoice.output_pdf(args.output_pdf.name)