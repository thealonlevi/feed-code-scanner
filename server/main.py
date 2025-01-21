import json
from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor
import sys
import os

# Load configuration
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading configuration: {e}")
    sys.exit(1)

# Extract configurations
VERIFY_TOKEN = config["verify_token"]
MAX_WORKERS = config["max_workers"]
SSL_CERT = config["ssl"]["cert"]
SSL_KEY = config["ssl"]["key"]
HOST = config.get("host", "0.0.0.0")
PORT = config.get("port", 443)

# Add project-specific imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from server.methods.get import GetMethod
from server.methods.post import PostMethod

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
        return GetMethod(request, VERIFY_TOKEN)
    
    elif request.method == 'POST':
        return PostMethod(request, executor)
    
    else:
        return "Method not allowed", 405

if __name__ == '__main__':
    # Run Flask app with SSL certificate
    app.run(
        host=HOST,
        port=PORT,
        ssl_context=(SSL_CERT, SSL_KEY)
    )
