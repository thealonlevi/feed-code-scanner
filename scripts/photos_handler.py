import requests
from PIL import Image
from io import BytesIO
import pytesseract
import re
from scripts.dynamodb_handler import add_event_to_code

def detect_embedded_code(extracted_text):
    """
    Detect an embedded code in the extracted text.

    Args:
        extracted_text (str): The text extracted from an image.

    Returns:
        str: The detected code if found, otherwise None.
    """
    # Define the regex for the embedded code
    code_pattern = r"\b(?=[A-Z0-9]{6}\b)(?=(?:.*[A-Z]){2,})(?=(?:.*\d){2,})[A-Z0-9]+\b"

    # Search for the code in the text
    match = re.search(code_pattern, extracted_text)

    if match:
        return f"{match.group(0)}"
    else:
        return None

def process_photo_event(event):
    """
    Process the photo event, download the image, extract text, and store the code in DynamoDB.
    """
    try:
        print("Processing Photo Event:")
        print(event)

        # Navigate to the photo data in the event
        for entry in event.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                photo_url = value.get("link")
                if not photo_url:
                    print("No photo URL found in the event.")
                    return
                
                # Download the image
                response = requests.get(photo_url)
                if response.status_code != 200:
                    print(f"Failed to download the image. Status code: {response.status_code}")
                    return
                
                # Load the image
                img = Image.open(BytesIO(response.content))

                # Perform OCR to extract text
                extracted_text = pytesseract.image_to_string(img)
                print("Extracted Text from Image:")
                print(extracted_text)
                
                # Detect the embedded code
                detected_code = detect_embedded_code(extracted_text)
                if detected_code:
                    print(f"DETECTED CODE: {detected_code}")
                    
                    # Store the code and event in DynamoDB
                    add_event_to_code(detected_code, event)
                    print(f"Stored event under code {detected_code} in DynamoDB.")
                else:
                    print("No valid code detected in the image.")

    except Exception as e:
        print(f"Error processing photo event: {e}")
