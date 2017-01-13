import boto3
import datetime
import sys

elb_name = sys.argv[1]

begining_of_today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

cw = boto3.client('cloudwatch')
metrics = cw.get_metric_statistics(
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

data_points = metrics['Datapoints']

sorted_data_points = sorted(data_points, key=lambda x: x['Timestamp'])

for e in sorted_data_points:
    print("%s, %d" % (e['Timestamp'].strftime('%Y/%m/%d'), e['Sum']))
