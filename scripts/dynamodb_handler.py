import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table_name = "scanned-codes"
table = dynamodb.Table(table_name)

def add_event_to_code(code, event):
    """
    Add an event to a code in the DynamoDB table.
    If the code does not exist, create a new item.
    """
    try:
        # Update the item (or create it if it doesn't exist)
        response = table.update_item(
            Key={"code": code},
            UpdateExpression="SET events = list_append(if_not_exists(events, :empty_list), :event)",
            ExpressionAttributeValues={
                ":empty_list": [],
                ":event": [event]
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Event added to code {code}. Updated item: {response['Attributes']}")
    except ClientError as e:
        print(f"Error adding event: {e.response['Error']['Message']}")

def get_events_by_code(code):
    """
    Retrieve all events associated with a code.
    """
    try:
        response = table.get_item(Key={"code": code})
        if "Item" in response:
            return response["Item"]
        else:
            print(f"No data found for code {code}.")
            return None
    except ClientError as e:
        print(f"Error retrieving events: {e.response['Error']['Message']}")
        return None

# Example usage
if __name__ == "__main__":
    test_code = "IE6O89"
    test_event = {
        "entry": [
            {
                "id": "517161164821567",
                "time": 1737458657,
                "changes": [
                    {
                        "value": {
                            "from": {"id": "517161164821567", "name": "Pituah"},
                            "link": "https://example.com/image.jpg",
                            "post_id": "517161164821567_122100491216739916",
                            "created_time": 1737458653,
                            "item": "photo",
                            "photo_id": "122100491162739916",
                            "published": 1,
                            "verb": "add"
                        },
                        "field": "feed"
                    }
                ]
            }
        ],
        "object": "page"
    }

    # Add the event to the code
    add_event_to_code(test_code, test_event)

    # Retrieve events for the code
    events = get_events_by_code(test_code)
    print(f"Events for code {test_code}: {events}")
