import os
import boto3
import datetime
from lib.item import Item

# get the costs for a period of time for a cost tag from AWS
class AwsItem(Item):
    profile = ''
    description = ''
    cost_tag = ''
    start = ''
    end = ''

    def __init__(self, profile, description, cost_tag, start, end, tax):
        os.environ['AWS_PROFILE'] = profile # set aws profile according to settings in invoices/customer.yaml
        formatted_date_start = datetime.datetime.strptime(start, '%Y-%m-%d').strftime('%d.%m.%Y')
        formatted_date_end = datetime.datetime.strptime(end, '%Y-%m-%d').strftime('%d.%m.%Y')
        self.description = description + " ("+formatted_date_start+" - "+formatted_date_end+")"
        self.cost_tag = cost_tag
        now = datetime.datetime.utcnow()
        self.set_amount(1)
        self.tax = tax
        if (start and end):
            self.start = start
            self.end = end
        else:
            self.start = now.replace(day=1).strftime('%Y-%m-%d')
            self.end = (datetime.date(now.year + now.month // 12, now.month % 12 + 1, 1) - datetime.timedelta(1)).strftime('%Y-%m-%d')
        self.get_costs_and_usage_from_aws()

    def get_costs_and_usage_from_aws(self):
        filterproject = {
            "Tags": {
                "Key": "Project",
                "Values": [
                    self.cost_tag,
                ]
            }
        }

        client = boto3.client('ce', 'eu-central-1')
        results = client.get_cost_and_usage(TimePeriod={'Start': self.start, 'End':  self.end}, Granularity='MONTHLY', Metrics=['UnblendedCost'], Filter=filterproject)
        self.total_price = round(float(results['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']), 2)
        self.price = self.total_price
        return self.calc_price()