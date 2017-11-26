# AWS Team cost reporter

A Simple command line tool for AWS Cost report

## What is this?
This tool is useful when multiple teams share one account and each team has an independent budget.
In one account, by default, costs of all teams are summed and reported, so each team can not know
the usage status and cost of their team.
In order to deal with it, AWS provices cost allocation tag.
http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html

This tool uses cost allocation tags.

This script repors each team cost and usage report with CSV format, using　AWS Cost Explorer API.
http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-explorer-api.html
Because of CE API need to access AWS North Virginia Region, you have to have access to
https://ce.us-east-1.amazonaws.com
(Thus, will not work on private, non-internet accessible environment.)

## Prerequests
1. Set up cost allocation tag.

http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html

2. Install boto3(aws sdk for python)

https://aws.amazon.com/sdk-for-python/?nc1=h_ls

## How to use

Super simple.

`team_cost_report.py -k "Cost Allocation Tag Key" -v "Cost Allocation Tag Value"` 

Example:
Suppose that cost allocation tag key is 'Project' and you work on 'NewWebProject', then.
`team_cost_report.py -k Project -v NewWebProject`
this will generate CSV file named `cost_report_2017-11-1-2017-11-25_NewWebProject.csv`



