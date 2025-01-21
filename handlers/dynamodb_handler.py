import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table_name = "scanned-codes"
table = dynamodb.Table(table_name)

def add_event_to_code(code, event):
    """
    Add an event to a code in the DynamoDB table.
    If the code does not exist, create a new item with the event.
    """
    try:
        # Update the item (or create it if it doesn't exist)
        print(f"Code: {code}")
        print(f"Event: {event}")
        response = table.update_item(
            Key={"codes": code},  # Ensure this matches the table's key schema
            UpdateExpression="SET events = list_append(if_not_exists(events, :empty_list), :new_event)",
            ExpressionAttributeValues={
                ":empty_list": [],
                ":new_event": [event]
            },
            ReturnValues="UPDATED_NEW"
        ) # THE ISSUE IS HERE, HOW DO WE DEBUG THIS??
        print(f"Event added to code {code}. Updated item: {response['Attributes']}")
    except ClientError as e:
        print(f"Error adding event: {e.response['Error']['Message']}")


def get_events_by_code(code):
    """
    Retrieve all events associated with a code from the DynamoDB table.
    """
    try:
        dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
        table_name = "scanned-codes"
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={"codes": code})  # Ensure this matches the table's key schema
        if "Item" in response:
            return response["Item"].get("events", [])
        else:
            print(f"No events found for code {code}.")
            return []
    except ClientError as e:
        print(f"Error retrieving events: {e.response['Error']['Message']}")
        return []