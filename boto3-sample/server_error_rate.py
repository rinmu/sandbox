# python get_cloudwatch_metrics.py RequestCount
# python get_cloudwatch_metrics.py HTTPCode_Backend_5XX

import boto3
import datetime
import sys
from IPython import embed

elb_name = sys.argv[1]

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
        StartTime=begining_of_today - datetime.timedelta(days=7),
        EndTime=begining_of_today,
        Period=86400,
        Statistics=['Sum'])

    return metrics['Datapoints']

def sum_list(data_points):
    sorted_data_points = sorted(data_points, key=lambda x: x['Timestamp'])
    print(sorted_data_points)
    return list(map(lambda x: (x['Timestamp'], x['Sum']), sorted_data_points))

requests = sum_list(get_data_points(elb_name, 'RequestCount'))
http_5xxs = sum_list(get_data_points(elb_name, 'HTTPCode_Backend_5XX'))

for i in range(len(requests)):
    date = requests[i][0].strftime('%Y/%m/%d')
    http_5xx = http_5xxs[i][1]
    request = requests[i][1]
    rate = float(http_5xx) / request
    print("%s, %f, %d, %d" % (date, rate, http_5xx, request))
