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
