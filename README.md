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

```
team_cost_report.py -k **Cost Allocation Tag Key** -v **Cost Allocation Tag Value**
```

Example 1:

Suppose that cost allocation tag key is **Project** and you work on **NewWebProject**, then.

`team_cost_report.py -k Project -v NewWebProject`

this will generate CSV file named `cost_report_2017-11-1-2017-11-25_NewWebProject.csv`

By default, this script set start date as first day of the month and end date as the day you type the command. if you would like to generate report on other day, use option `-s` and `-e`.


Example 2:

Today is Nov 26, 2017, and suppose you want to know the cost report at 2 month ago ( Sep 1, 2017 - Sep 30, 2017) on your project, then

`team_cost_report.py -k Project -v NewWebProject -s 2017-09-01 -e 2017-09-30`

Make sure the date format is **yyyy-mm-dd**. 
