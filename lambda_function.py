import boto3, json,datetime
import copy
import os 

def lambda_handler(event, context):
    
        s3BucketName = event['s3BucketName']
        REGION_NAME  = event['REGION_NAME']
        ARN          = event['ARN']

        sns_client = boto3.client('sns', REGION_NAME)



        response= sns_client.get_topic_attributes(
            TopicArn= ARN
        )

        policy = json.dumps(response)
        resp = json.loads(policy)

        policy_string = resp["Attributes"]["Policy"]
        policy = json.loads(policy_string)
        #print(polåicy["Statement"])

        statement0 = policy["Statement"][0]
        obj = copy.deepcopy(statement0)

        obj["Condition"]["ArnLike"]["aws:SourceArn"] = "arn:aws:s3:*:*:" + s3BucketName
        obj["Sid"] = str(datetime.datetime.now())



        policy["Statement"].append(obj)
        #pprint(policy["Statement"])



        sns_client.set_topic_attributes( TopicArn = ARN , 
                                        AttributeName = "Policy" , 
                                        AttributeValue = json.dumps(policy)
                                        )

        s3 = boto3.resource('s3')
        bucket_notification = s3.BucketNotification(s3BucketName)
        response = bucket_notification.put(
            NotificationConfiguration={
                'TopicConfigurations': [
                    {
                        'Id': 'mynotfication',
                        'TopicArn': ARN,
                        'Events': [
                            's3:ObjectCreated:*',
                        ],
                        'Filter': {
                            'Key': {
                                'FilterRules': [
                                    {
                                        'Name': 'prefix',
                                        'Value': 'my-filter'
                                },
                                ]
                            }
                        }
                    },
                ],
            }
        )        






        return response



