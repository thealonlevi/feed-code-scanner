import pytesseract

def detect_text(img):
    # Perform OCR to extract text
    extracted_text = pytesseract.image_to_string(img)
    print("Extracted Text from Image:")
    print(extracted_text)
    return extracted_text