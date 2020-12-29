#!/usr/bin/env python3

from lib.invoice import Invoice
from lib.item import Item
import argparse
import locale


parser = argparse.ArgumentParser(description='Convert HTML template to pdf with data from yaml')
parser.add_argument('--template', help='The name of the template to use (e.g. invoice)', default="invoice.html")
parser.add_argument('--data', help='The name of the data template to use (e.g. invoices/customer.yaml)', default="invoices/test.yaml")
parser.add_argument('--output', help='The output pdf file', default="invoice.pdf", type=argparse.FileType('w'))
parser.add_argument('--locale', help='The locale to use', default="de_DE.UTF-8")

args = parser.parse_args()
locale.setlocale(locale.LC_ALL, args.locale)

invoice = Invoice(args.data)
invoice.add_item(Item("Random Item", 25.00, 2, 0))
invoice.output_pdf(args.output.name)