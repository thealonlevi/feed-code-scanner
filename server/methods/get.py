import json
from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor
import sys
import os

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Extract configurations
VERIFY_TOKEN = config["verify_token"]
MAX_WORKERS = config["max_workers"]
SSL_CERT = config["ssl"]["cert"]
SSL_KEY = config["ssl"]["key"]

# Add project-specific imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.event_sorter import sort_event
from handlers.photos_handler import process_photo_event

# Initialize Flask app
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)  # Dynamically set from config

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
                executor.submit(process_photo_event, event)
            executor.submit(sort_event, event)
            return "Event sorting initiated", 200
        
        return "Invalid event", 400
    
    else:
        return "Method not allowed", 405

if __name__ == '__main__':
    # Run Flask app with SSL certificate
    app.run(
        host='0.0.0.0',
        port=443,
        ssl_context=(SSL_CERT, SSL_KEY)
    )


def GetMethod(request, VERIFY_TOKEN):
    print("GET request received.")
    print("Headers:", request.headers)
    print("Query Parameters:", request.args)
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Forbidden", 403