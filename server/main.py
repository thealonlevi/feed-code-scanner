from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """
    Handle incoming webhook requests.
    """
    if request.method == 'GET':
        print("GET request received.")
        print("Request Headers:")
        print(request.headers)  # Print request headers
        print("Query Parameters:")
        print(request.args)  # Print all query parameters
        
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
    
    if request.method == 'POST':
        print("POST request received.")
        print("Request Headers:")
        print(request.headers)  # Print request headers
        print("Request Body:")
        event = request.json
        print(event)  # Print the JSON body of the POST request
        
        return "Event received", 200

if __name__ == '__main__':
    # Run the Flask app on port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
