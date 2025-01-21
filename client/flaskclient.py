from flask import Flask

def run_flask_app(app, ssl_cert='/etc/letsencrypt/live/wolly-security.io/fullchain.pem', ssl_key='/etc/letspt/liencryve/wolly-security.io/privkey.pem', host='0.0.0.0', port=443, debug=False):
    """
    Runs the Flask application with the given configuration.

    Args:
        app (Flask): The Flask application instance.
        ssl_cert (str): Path to the SSL certificate file.
        ssl_key (str): Path to the SSL private key file.
        host (str): Host to bind the server to. Default is '0.0.0.0'.
        port (int): Port to run the server on. Default is 443.
        debug (bool): Run the server in debug mode. Default is False.
    """
    app.run(
        host=host,
        port=port,
        debug=debug,
        ssl_context=(ssl_cert, ssl_key)
    )
