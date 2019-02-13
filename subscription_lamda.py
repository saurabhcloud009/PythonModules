
import boto3, json
REGION_NAME = "us-east-2"
ARNS = [ 'arns']
sns_client = boto3.client('sns', REGION_NAME)

for ARN in ARNS:
    print (ARN)

response = sns_client.subscribe(
    TopicArn='topicarn',
    Protocol='lambda',
    Endpoint= ARN
    
)