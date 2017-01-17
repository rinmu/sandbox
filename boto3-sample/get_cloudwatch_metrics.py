# python get_cloudwatch_metrics.py RequestCount
# python get_cloudwatch_metrics.py HTTPCode_Backend_5XX

import boto3
import datetime
import sys

elb_name = sys.argv[1]
metrics_name = sys.argv[2]

begining_of_today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

def get_data_points(elb_name, metrics_name):
    cw = boto3.client('cloudwatch')
    metrics = cw.get_metric_statistics(
                Namespace='AWS/ELB',
                MetricName=metrics_name,
                Dimensions=[
                    {
                        'Name': 'LoadBalancerName',
                        'Value': elb_name
                    }
                ],
                StartTime=begining_of_today - datetime.timedelta(days=30),
                EndTime=begining_of_today,
                Period=86400,
                Statistics=['Sum'])

    return metrics['Datapoints']

data_points = get_data_points(elb_name, metrics_name)

sorted_data_points = sorted(data_points, key=lambda x: x['Timestamp'])

for e in sorted_data_points:
    print("%s, %d" % (e['Timestamp'].strftime('%Y/%m/%d'), e['Sum']))
