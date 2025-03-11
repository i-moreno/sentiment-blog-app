import boto3

dynamo = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamo.Table('BlogAppTable')
