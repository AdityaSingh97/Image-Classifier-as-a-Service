import boto3

#loading sqs
sqs_resource = boto3.resource('sqs')
sqs_client = boto3.client('sqs')

#loading s3 bucket
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
response = s3.list_buckets()

def create_queue(queue_name, attributes):
    SQS_QUEUE_NAME = queue_name
    # Create a SQS queue
    response = sqs_client.create_queue(
        QueueName=SQS_QUEUE_NAME, Attributes=attributes)
    return response['QueueUrl']


def get_queue_url(queue_name):
    return sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']


def get_queue_attributes(queue_url):
    # for visible and invisible -> attribute_names = ['All']
    queue_attrs = sqs_client.get_queue_attributes(
        QueueUrl=queue_url, AttributeNames=['All'])
    if 'Attributes' in queue_attrs:
        return queue_attrs['Attributes']
    else:
        return {}


def get_one_queue_attribute(queue_url, attribute_name='ApproximateNumberOfMessages'):
    attrs = get_queue_attributes(queue_url)
    if attribute_name in attrs:
        return attrs[attribute_name]
    else:
        return '-'


# send message to queue
def send_message(queue_url, message_attributes, message_group_id, message_body):
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageAttributes=message_attributes,
        MessageGroupId=message_group_id,
        MessageBody=message_body
    )
    return response['MessageId']


# recieve message from queue (wait time as a variable)
def receive_message(queue_url, num_messages):
    return sqs_client.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=num_messages,
    )


def delete_message(queue_url, receipt_handle):
    sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )


