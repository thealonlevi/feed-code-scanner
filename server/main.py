from flask import Flask, request

app = Flask(__name__)

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
        VERIFY_TOKEN = "my_custom_verify_token_12345"  # Replace with your verification token
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("Webhook verified successfully.")
            return challenge, 200
        else:
            print("Webhook verification failed.")
            return "Forbidden", 403
    elif request.method == 'POST':
        print("POST request received.")
        print("Headers:", request.headers)
        print("Body:", request.get_json())
        return "Event received", 200
    else:
        print(f"Unhandled HTTP method: {request.method}")
        return "Method not allowed", 405

if __name__ == '__main__':
    # Run Flask app with SSL certificate
    app.run(host='0.0.0.0', port=443, ssl_context=(
        '/etc/letsencrypt/live/wolly-security.io/fullchain.pem',
        '/etc/letsencrypt/live/wolly-security.io/privkey.pem'
    ))
