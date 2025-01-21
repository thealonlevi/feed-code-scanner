import requests
from PIL import Image
from io import BytesIO
import pytesseract

def process_photo_event(event):
    """
    Process the photo event, download the image, and extract text.
    """
    try:
        # Ensure the event is structured properly
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

    except Exception as e:
        print(f"Error processing photo event: {e}")
