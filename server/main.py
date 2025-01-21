from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.event_sorter import sort_event
from scripts.photos_handler import process_photo_event
import boto3
from botocore.exceptions import ClientError
import logging
logging.basicConfig(level=logging.DEBUG)
boto3.set_stream_logger('botocore', level=logging.DEBUG)

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table_name = "scanned-codes"
table = dynamodb.Table(table_name)

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=5)  # Adjust the number of workers as needed

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """
    Handle incoming webhook requests.
    """
    print("REQUEST RECEIVED")
    
    if request.method == 'GET':
        print("GET request received.")
        print("Headers:", request.headers)
        print("Query Parameters:", request.args)
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        VERIFY_TOKEN = "my_custom_verify_token_12345"
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403
    
    elif request.method == 'POST':
        print("POST request received.")
        print("Headers:", request.headers)
        print("Body:", request.get_json())
        
        event = request.get_json()
        
        # Sort the event and process asynchronously
        if event:
            outp = sort_event(event)
            if outp == "photo":
                executor.submit(process_photo_event, event, table)
            executor.submit(sort_event, event)
            return "Event sorting initiated", 200
        
        return "Invalid event", 400
    
    else:
        return "Method not allowed", 405

if __name__ == '__main__':
    # Run Flask app with SSL certificate
    app.run(host='0.0.0.0', port=443, ssl_context=(
        '/etc/letsencrypt/live/wolly-security.io/fullchain.pem',
        '/etc/letsencrypt/live/wolly-security.io/privkey.pem'
    ))