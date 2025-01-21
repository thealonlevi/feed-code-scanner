from flask import Flask, request

app = Flask(__name__)

@app.before_request
def log_request_info():
    """
    Log all incoming requests regardless of method.
    """
    print("=== REQUEST RECEIVED ===")
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print("Headers:")
    print(request.headers)  # Log headers
    print("Query Parameters:")
    print(request.args)  # Log query parameters
    print("Body:")
    try:
        print(request.get_data(as_text=True))  # Log raw body
    except Exception as e:
        print(f"Failed to read body: {e}")

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """
    Handle incoming webhook requests.
    """
    if request.method == 'GET':
        print("GET request processing started.")
        
        # Verification endpoint for webhook setup
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        print(f"Mode: {mode}, Token: {token}, Challenge: {challenge}")

        VERIFY_TOKEN = "my_custom_verify_token_12345"  # Replace with your verification token

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("Webhook verified successfully.")
            return challenge, 200
        else:
            print("Webhook verification failed.")
            return "Forbidden", 403

    elif request.method == 'POST':
        print("POST request processing started.")

        # Handle webhook event
        try:
            event = request.json
            print("Webhook Event Received:", event)  # Print the event
        except Exception as e:
            print(f"Failed to parse JSON body: {e}")

        return "Event received", 200

    else:
        print(f"Unhandled HTTP method: {request.method}")
        return f"Method {request.method} not allowed.", 405

if __name__ == '__main__':
    # Run the Flask app on port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
