#!/usr/bin/env python3

from lib.aws_item import AwsItem
from lib.invoice import Invoice
from lib.item import Item
import boto3
import datetime
import argparse
import locale


parser = argparse.ArgumentParser(description='Convert HTML template to pdf with data from yaml')
parser.add_argument('--template', help='The name of the template to use (e.g. invoice)', default="invoice.html")
parser.add_argument('--data', help='The name of the data template to use (e.g. invoices/customer.yaml)', default="invoices/test.yaml")
parser.add_argument('--output', help='The output pdf file', default="invoice.pdf", type=argparse.FileType('w'))
parser.add_argument('--locale', help='The locale to use', default="de_DE.UTF-8")
parser.add_argument('--fromDate', help='from what date', default='2021-01-01')
parser.add_argument('--toDate', help='to what date', default='2021-12-31')
parser.add_argument('--overrideTax', help='overridden tax', default='')
parser.add_argument('--overrideInvoiceDate', help='invoice´s date', default='')
parser.add_argument('--overrideInvoiceNumber', help='invoice´s number', default='')
parser.add_argument('--creditNumber', help='credit´s number', default='')

args = parser.parse_args()

locale.setlocale(locale.LC_ALL, args.locale)

now = datetime.datetime.utcnow()

invoice = Invoice(args.data, fromDate=args.fromDate, toDate=args.toDate, template=args.template, overrideInvoiceDate=args.overrideInvoiceDate, overrideInvoiceNumber=args.overrideInvoiceNumber, overrideTax=args.overrideTax, creditNumber=args.creditNumber)
invoice.output_pdf(args.output.name)