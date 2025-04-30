import json
import boto3
import urllib3
import os
from datetime import datetime

# Create an HTTP client (for sending Slack messages)
http = urllib3.PoolManager()

# Load environment variables (set these in Lambda configuration)
DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

# Create AWS service clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # Log incoming event

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        timestamp = datetime.utcnow().isoformat()

        print(f"File uploaded: {key} in bucket: {bucket} at {timestamp}")

        # 1. Save metadata to DynamoDB
        try:
            table.put_item(
                Item={
                    'fileName': key,
                    'bucketName': bucket,
                    'uploadTimestamp': timestamp
                }
            )
            print("Saved to DynamoDB")
        except Exception as e:
            print("Error saving to DynamoDB:", str(e))

        # 2. Send notification to Slack
        try:
            message = f"S3 Upload Detected\nBucket: {bucket}\nFile: {key}\nTime: {timestamp}"
            slack_payload = {'text': message}
            http.request(
                'POST',
                SLACK_WEBHOOK_URL,
                body=json.dumps(slack_payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            print("Slack notification sent")
        except Exception as e:
            print("Error sending Slack notification:", str(e))

        # 3. Publish notification to SNS
        try:
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message
            )
            print("SNS notification published")
        except Exception as e:
            print("Error publishing to SNS:", str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('Processed successfully')
    }
