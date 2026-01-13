import json
import boto3

# Initialize the SNS client
sns = boto3.client('sns')


TOPIC_ARN = "arn:aws:sns:us-east-1:801441827431:Serverless-text"


def lambda_handler(event, context):
    try:
        # 1. Parse the incoming request
        # If running a simple test, 'message' might be passed directly
        # If running from API Gateway (later), it's inside 'body'
        if 'body' in event:
            body = json.loads(event['body'])
            message_text = body.get('message', 'Default message from Lambda')
            subject_text = body.get('subject', 'AWS Alert')
        else:
            # Fallback for simple testing
            message_text = event.get('message', 'Default message from Lambda')
            subject_text = event.get('subject', 'AWS Alert')

        # 2. Publish to the SNS Topic
        response = sns.publish(
            TopicArn=TOPIC_ARN,
            Message=message_text,
            Subject=subject_text
        )

        # 3. Return success
        return {
            'statusCode': 200,
            'body': json.dumps(f"Message published! ID: {response['MessageId']}")
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }