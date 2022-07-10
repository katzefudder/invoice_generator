#!/bin/bash

# displays the last month's costs in USD for tagged resources
# https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html

# FIRST=$(date --date="$(date +'%Y-%m-01') - 1 month" +%s) # date on general Linux distributions
# LAST=$(date --date="$(date +'%Y-%m-01') - 1 second" +%s)

PROJECT=project_key

FIRST=$(date -v1d -v-1m +%Y-%m-%d) # date on Mac OS X
LAST=$(date -v1d -v-1d +%Y-%m-%d)

aws ce get-cost-and-usage --time-period Start=$FIRST,End=$LAST --granularity=MONTHLY  --metrics BlendedCost --filter '{"Tags": {"Key": "Project","Values": ["'$PROJECT'"]}}' | jq -r '.ResultsByTime[].Total.BlendedCost.Amount'