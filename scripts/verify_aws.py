import boto3

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')

try:
    tables = list(dynamodb.tables.all())
    print("Available tables:", tables)
except Exception as e:
    print("Error accessing DynamoDB:", e)
