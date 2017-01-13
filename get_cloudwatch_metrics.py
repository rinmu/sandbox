import boto3
import datetime
import sys
import pprint

elb_name = sys.argv[1]

pp = pprint.PrettyPrinter(indent=4)

begining_of_today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

cw = boto3.client('cloudwatch')
get_metric_statistics = cw.get_metric_statistics(
                            Namespace='AWS/ELB',
                            MetricName='HTTPCode_Backend_5XX',
                            Dimensions=[
                                {
                                    'Name': 'LoadBalancerName',
                                    'Value': elb_name
                                }
                            ],
                            StartTime=begining_of_today - datetime.timedelta(days=14),
                            EndTime=begining_of_today,
                            Period=86400,
                            Statistics=['Sum'])

pp.pprint(get_metric_statistics)
