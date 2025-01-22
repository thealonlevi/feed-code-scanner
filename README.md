# Feed Code Monitor

Feed Code Monitor is a web application designed to monitor and handle photo events, extract embedded codes from images, and manage related data using AWS DynamoDB. The application is built using Flask and includes integrations with the Facebook Graph API and OCR functionalities.

---

## Features

- **Webhook Handling**:
  - Processes `GET` and `POST` requests from Facebook's Webhooks API.
  - Extracts and processes photo events asynchronously using a thread pool.

- **OCR and Code Detection**:
  - Uses `pytesseract` and `OpenCV` to extract and detect embedded codes in images.

- **Facebook Post Insights**:
  - Fetches post impressions using the Facebook Graph API and updates records in DynamoDB.

- **AWS DynamoDB Integration**:
  - Stores codes, events, and calculated post impressions.
  - Securely fetches and updates records in the `scanned-codes` and `variables` DynamoDB tables.

- **Configuration Management**:
  - Reads application configurations (e.g., SSL paths, tokens) from `config/config.json`.

---

## Project Structure

```plaintext
feed-code-monitor/
├── config/
│   └── config.json                 # Configuration file for tokens, SSL paths, and settings.
├── handlers/
│   ├── dynamodb_handler.py         # Handles DynamoDB interactions.
│   └── photos_handler.py           # Processes photo-related events and extracts codes.
├── scripts/
│   ├── code_detection.py           # Detects embedded codes from extracted text.
│   ├── event_sorter.py             # Routes and processes incoming events.
│   └── text_extraction.py          # Handles OCR and text extraction from images.
├── server/
│   ├── methods/
│   │   ├── get.py                  # Handles GET requests for the webhook.
│   │   └── post.py                 # Handles POST requests for the webhook.
│   └── main.py                     # Entry point for the Flask application.
├── .gitignore                      # Files and folders to ignore in Git.
├── requirements.txt                # Python dependencies for the project.
└── README.md                       # Project documentation.
```

---

## Setup Instructions

### 1. Create an Inbound Rule for Port 8080 (TCP)

- Update your server’s security/firewall settings to **allow inbound traffic** on port **8080** (TCP).  
- If you’re on AWS, this means updating your **Security Group** to include a rule for inbound traffic on port **8080**.

### 2. Create or Obtain SSL Certificates

- If you plan to serve your application over HTTPS, you’ll need valid SSL certificates.
- Store the certificate (`.crt`) and key (`.key`) paths in the `config/config.json` file under something like:

```json
{
  "ssl_certificate_path": "/path/to/your/certificate.crt",
  "ssl_key_path": "/path/to/your/key.key",
  ...
}
```

- If you do not require HTTPS, you can ignore or leave these fields blank, depending on your setup.

### 3. Install AWS CLI & Configure It

1. **Install AWS CLI** (Example for Ubuntu/Debian):
   ```bash
   sudo apt-get update
   sudo apt-get install awscli
   ```
2. **Configure AWS CLI** with **sudo** (required):
   ```bash
   sudo aws configure
   ```
   - Enter your AWS **Access Key**, **Secret Access Key**, default region, and output format (e.g., `json`) when prompted.
   - This is necessary so the application can access AWS DynamoDB.

### 4. Set Up Python Virtual Environment and Dependencies

1. **Install Python 3 and Virtual Environment Tools** (if not already installed):
   ```bash
   sudo apt-get install python3 python3-venv
   ```
2. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   - This installs Flask, pytesseract, OpenCV, boto3, and other required libraries.

### 5. Configure `config.json`

Open the file `config/config.json` and add the required values. For instance:

```json
{
  "ssl_certificate_path": "/path/to/ssl_certificate.crt",
  "ssl_key_path": "/path/to/ssl_key.key",
  "facebook_verification_token": "<your_facebook_verification_token>",
  "facebook_page_token": "<your_facebook_page_token>",
  "aws_region": "us-east-1",
  "dynamodb_tables": {
    "scanned_codes": "scanned-codes",
    "variables": "variables"
  }
}
```

- `ssl_certificate_path` and `ssl_key_path` are used if you run HTTPS directly from Flask.  
- `facebook_verification_token` and `facebook_page_token` are required if you’re integrating with Facebook’s Webhooks and Graph API.  
- `aws_region` should match the region of your DynamoDB tables.  
- `dynamodb_tables` indicates which table names to use for storing and retrieving codes/variables.

### 6. Run the Application

1. **Start the Flask Application** using **sudo** (required):
   ```bash
   sudo venv/bin/python server/main.py
   ```
   - The app will typically listen on port **8080** (depending on your configuration).

2. **Access the Application**:
   - Facebook API will communicate only through HTTPS (Flask SSL config is required), visit:  
     `https://<your-server-ip>:8080/` <- Advised to use a Domain with a SSL certificate, and implement an A record pointing to your server's IP,
     and then using that domain as the endpoint which you provide to Facebook.

---

## Additional Tips

- **System Dependencies for OCR**:
  - Make sure **Tesseract** OCR engine is installed if you want to extract text from images:
    ```bash
    sudo apt-get install tesseract-ocr
    ```
- **Facebook Webhook Verification**:
  - Ensure your **webhook callback** is set to your server’s `/webhook` endpoint (or similar) in the Facebook app settings.
  - Use the same **verification token** you set in your `config.json`.
- **Production Use**:
  - For production, consider placing this Flask app behind a web server like **Nginx** or **Apache** and possibly use **Gunicorn** or **uWSGI**.
  - For example:
    ```bash
    sudo venv/bin/gunicorn --bind 0.0.0.0:8080 main:app
    ```
  - Terminate SSL in Nginx/Apache for better performance and easier certificate management.

---

## Summary

1. **Open port 8080** for inbound traffic.  
2. **Use `sudo`** when installing AWS CLI and configuring it (`sudo aws configure`).  
3. **Create a Python virtual environment** and install the dependencies.  
4. **Update `config/config.json`** for SSL paths, Facebook tokens, and AWS settings.  
5. **Run the Flask app with `sudo`** (e.g., `sudo venv/bin/python server/main.py`).  
6. **Monitor logs** to ensure photo events, OCR, and DynamoDB operations are working as intended.

This completes your setup for **Feed Code Monitor**!

## Potential Vulnerabilities on transition to PRODUCTION

1. scripts/text_extraction.py extracts texts from images it receives, however, it does not do it very thoroughly, and it often makes mistakes.
   SOLUTION: Needs to be recreated in a way where it can consistently and accurately extract the embedded code.
2. [ON-CLOUD] AWS Lambda Function postImpressionScript(serverless) makes a request for every post under every code stored in the "scanned-codes"
   DynamoDB. The more posts that accumulate there, the more likely this script is to crash or cause Facebook's API to rate-limit you.
   SOLUTION: Needs to be recreated, preferably on the server and not on the cloud, and it needs to be configured to make the requests based on
   the defined limits of Facebook's API, and perhaps send out the requests asynchronously(within the liimts of Facebook's API) to save time
   while gathering the information, as this is a long task(depending on the amount of posts).
   ADVISE: Systematically prioritize posts to gather information for, in a case of a queue of tasks, and create a manager which manages
   instances which are making the requests and knows which requests to prioritize in the queue, and which to not. 
