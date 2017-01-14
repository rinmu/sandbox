import boto3
import pprint

pp = pprint.PrettyPrinter(indent=4)

cloud_watch = boto3.client('cloudwatch')

list_metrics = cloud_watch.list_metrics(Namespace='AWS/ELB')['Metrics']

pp.pprint(set(map(lambda e: e['MetricName'], list_metrics)))
