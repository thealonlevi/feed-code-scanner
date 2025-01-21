from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """
    Handle incoming webhook requests.
    """
    if request.method == 'GET':
        print(request.json)
        # Verification endpoint for webhook setup
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        VERIFY_TOKEN = "your_verify_token_here"  # Replace with your verification token

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("Webhook verified successfully.")
            return challenge, 200
        else:
            print("Webhook verification failed.")
            return "Forbidden", 403
    
    if request.method == 'POST':
        # Handle webhook event
        event = request.json
        print("Webhook Event Received:", event)  # Print the event
        return "Event received", 200

if __name__ == '__main__':
    # Run the Flask app on port 80
    app.run(host='0.0.0.0', port=8080, debug=True)
