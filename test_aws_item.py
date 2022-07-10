import os
import pytest
from lib.aws_item import AwsItem

def test_aws_invoice(mocker):
    mocker.patch('lib.aws_item.AwsItem.get_costs_and_usage_from_aws', return_value=None)
    item = AwsItem('testing_aws_profile', 'testing', 'cost-tag', "2022-06-01", "2022-06-30", 19)
    assert item.get_description() == 'testing (01.06.2022 - 30.06.2022)'
    assert item.get_amount() == 1
    assert item.get_tax() == 19
    assert os.environ['AWS_PROFILE'] == "testing_aws_profile"
    assert item.get_costs_and_usage_from_aws() == None
