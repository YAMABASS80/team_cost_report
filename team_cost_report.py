'''
[AWS Cost Report Tool]
This tool is useful when multiple teams share one account and each team has an independent budget.
In one account, by default, costs of all teams are summed and reported, so each team can not know
the usage status and cost of their team.
In order to deal with it, AWS provices cost allocation tag.
http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html
This tool uses cost allocation tags.

This script repors each team cost and usage report with CSV format, using AWS Cost Explorer API.
http://docs.aws.amazon.com/ja_jp/awsaccountbilling/latest/aboutv2/cost-explorer-api.html
Because of CE API need to access AWS North Virginia Region, you have to have access to
https://ce.us-east-1.amazonaws.com
(Thus, will not work on private, non-internet accessible environment.)
'''
import csv
import argparse
from datetime import datetime as dt
import boto3

parser = argparse.ArgumentParser(
    description='Team cost report tool'
)
parser.add_argument(
    '-k', '--tag-key',
    action='store',
    dest='tag_key',
    required=True,
    help='Specify resource tag key represents your team. ex) Project'
)
parser.add_argument(
    '-v', '--tag-value',
    action='store',
    dest='tag_value',
    required=True,
    help='Specify resource tag value represents your team. ex) Web, Finance'
)
parser.add_argument(
    '-s', '--start-date',
    action='store',
    dest='start_date',
    default=dt.now().strftime("%Y-%m-01"),
    help='cost report start date with yyyy-mm-dd format. Default = the first day of the month.'
)
parser.add_argument(
    '-e', '--end-date',
    action='store',
    dest='end_date',
    default=dt.now().strftime("%Y-%m-%d"),
    help='cost report end date with yyyy-mm-dd format. Default = today.'
)

args = parser.parse_args()
tag_key = args.tag_key
tag_value = args.tag_value
start_date = args.start_date
end_date = args.end_date

ce = boto3.client('ce', region_name='us-east-1')
query = {
    "TimePeriod" : {
        "Start" : start_date,
        "End": end_date
    },
    "Granularity" : "MONTHLY",
    "Filter" : {
        "Tags" : {
            "Key" : tag_key,
            "Values" : [
                tag_value
            ]
        }
    },
    "Metrics" :["BlendedCost", "UnblendedCost", "UsageQuantity"],
    "GroupBy" : [
        {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
        },
        {
            'Type': 'DIMENSION',
            'Key': 'USAGE_TYPE'
        }
    ]
}
response = ce.get_cost_and_usage(**query)

def get_header(response):
    '''
    Response will be like below.
    | SERVICE | USAGE_TYPE | BlendedCost | UnblendedCost | UsageQuantity |
    '''
    _header = [_key['Key'] for _key in response['GroupDefinitions']]
    _header.extend(response['ResultsByTime'][0]['Groups'][0]['Metrics'].keys())
    return _header

def get_record(group, header):
    '''
    In order to write csv via DictWriter class, this returns a dictionaly object as below.
    {
        'SERVICE' : service_name,
        'USAGE_TYPE' : usage_type,
        'BlendedCost' : blended_cost,
        (according to 'header' as defined by get_header)
    }
    '''
    record = {}
    # Keys : such as SERVICE_NAME, USAGE_TYPE
    record = dict(zip(header, group['Keys']))

    # Metrics : such as blended cost
    metrics = group['Metrics']
    for _h in header:
        _v = metrics.get(_h)
        if _v is not None:
            record[_h] = _v['Amount']
    return record

if __name__ == '__main__':
    with open('cost_report_' + start_date + '-' + end_date + '_' + tag_value + '.csv', 'wb') as f:
        header = get_header(response)
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for group in response["ResultsByTime"][0]["Groups"]:
            record = get_record(group, header)
            writer.writerow(record)
