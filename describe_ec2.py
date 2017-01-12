import boto3

client = boto3.client('ec2', region_name='ap-northeast-1')
response = client.describe_instances()
print(response)
