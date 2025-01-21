import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB resource
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
        response = table.update_item(
            Key={"codes": {"S": code}},
            UpdateExpression="SET events = list_append(if_not_exists(events, :empty_list), :event)",
            ExpressionAttributeValues={
                ":empty_list": {"L": []},
                ":event": {"L": [{"M": event}]}
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Event added to code {code}. Updated item: {response['Attributes']}")
    except ClientError as e:
        print(f"Error adding event: {e.response['Error']['Message']}")


def get_events_by_code(code):
    """
    Retrieve all events associated with a code from the DynamoDB table.
    """
    try:
        response = table.get_item(Key={"codes": {"S": code}})
        if "Item" in response:
            return response["Item"].get("events", {}).get("L", [])
        else:
            print(f"No events found for code {code}.")
            return []
    except ClientError as e:
        print(f"Error retrieving events: {e.response['Error']['Message']}")
        return []


# Example usage
if __name__ == "__main__":
    test_code = "IE6O89"
    test_event = {
        "entry": [
            {
                "id": {"S": "517161164821567"},
                "time": {"N": "1737458657"},
                "changes": [
                    {
                        "value": {
                            "from": {"id": {"S": "517161164821567"}, "name": {"S": "Pituah"}},
                            "link": {"S": "https://example.com/image.jpg"},
                            "post_id": {"S": "517161164821567_122100491216739916"},
                            "created_time": {"N": "1737458653"},
                            "item": {"S": "photo"},
                            "photo_id": {"S": "122100491162739916"},
                            "published": {"N": "1"},
                            "verb": {"S": "add"}
                        },
                        "field": {"S": "feed"}
                    }
                ]
            }
        ],
        "object": {"S": "page"}
    }

    # Add the event to the code
    add_event_to_code(test_code, test_event)

    # Retrieve events for the code
    events = get_events_by_code(test_code)
    print(f"Events for code {test_code}: {events}")
