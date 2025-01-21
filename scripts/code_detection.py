import re

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
