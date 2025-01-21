import re
import requests
from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
import pytesseract
import platform

# Dynamically set the Tesseract-OCR executable path based on the OS
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def preprocess_image(image):
    """
    Preprocess the image to improve OCR detection.
    """
    # Convert to grayscale
    image = ImageOps.grayscale(image)
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    # Binarize the image (convert to black and white)
    threshold = 128
    image = image.point(lambda p: p > threshold and 255)
    # Resize to increase clarity
    image = image.resize((image.width * 3, image.height * 3), Image.Resampling.LANCZOS)
    return image


def process_webhook_event(event):
    """
    Process the Webhook event to download the photo and scan for an embedded code.
    """
    # Extract relevant data from the event
    entry = event.get('entry', [])[0]
    changes = entry.get('changes', [])[0]
    value = changes.get('value', {})
    
    photo_url = value.get('link')
    post_id = value.get('post_id')
    publisher_name = value.get('from', {}).get('name', 'Unknown Publisher')
    created_time = value.get('created_time', 'Unknown Time')
    
    if not photo_url:
        print("No photo URL found in the event.")
        return
    
    # Download the photo
    response = requests.get(photo_url)
    if response.status_code != 200:
        print(f"Failed to download the image. Status code: {response.status_code}")
        return
    
    # Load and preprocess the image
    try:
        img = Image.open(BytesIO(response.content))
        img = preprocess_image(img)
        # Save preprocessed image for debugging
        img.save("preprocessed_image.png")
        print("Preprocessed image saved for debugging.")
    except Exception as e:
        print(f"Error loading or preprocessing image: {e}")
        return
    
    # Perform OCR using pytesseract
    try:
        extracted_text = pytesseract.image_to_string(img)
        print(f"Extracted Text: {extracted_text}")
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return
    
    # Search for the embedded code (6 alphanumeric characters)
    code_pattern = r'\b[A-Za-z0-9]{6}\b'
    match = re.search(code_pattern, extracted_text)
    
    if match:
        embedded_code = match.group(0)
        print(f"Embedded Code Found: {embedded_code}")
    else:
        embedded_code = "No code found"
        print("No embedded code detected in the image.")
    
    # Simulate storing data in a database
    record = {
        "post_id": post_id,
        "publisher_name": publisher_name,
        "created_time": created_time,
        "embedded_code": embedded_code,
        "photo_url": photo_url,
    }
    print("Record saved:", record)


# Example Webhook Event
webhook_event = {'entry': [{'id': '517161164821567', 'time': 1737386618, 'changes': [{'value': {'from': {'id': '517161164821567', 'name': 'Pituah'}, 'link': 'https://scontent.ftlv27-1.fna.fbcdn.net/v/t39.30808-6/473740178_122099790386739916_72755353017980701_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e5c1b6&_nc_ohc=6BaDdHKI0i0Q7kNvgEUmTOU&_nc_zt=23&_nc_ht=scontent.ftlv27-1.fna&_nc_gid=AQEMD5kDWXxfAQxCczn6jen&oh=00_AYC8MI7D-Om6oYirLPSi4qvrb3PdY2dlIkx5qUALJQcP-A&oe=67944EFA', 'post_id': '517161164821567_122099790404739916', 'created_time': 1737386614, 'item': 'photo', 'photo_id': '122099790380739916', 'published': 1, 'verb': 'add'}, 'field': 'feed'}]}], 'object': 'page'}

# Run the script with the example event
process_webhook_event(webhook_event)
