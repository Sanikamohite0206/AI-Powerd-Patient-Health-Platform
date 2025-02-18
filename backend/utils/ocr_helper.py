import pytesseract
import requests
import cv2
import numpy as np
from PIL import Image
import re

# Set Tesseract path (Windows only)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def fetch_image_from_url(image_url):
    """Fetch image from a URL and convert it to OpenCV format"""
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    
    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

def preprocess_image(image):
    """Convert image to grayscale and apply thresholding"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_text_from_image(image_url):
    """Extract text from an image using Tesseract OCR"""
    image = fetch_image_from_url(image_url)
    processed_image = preprocess_image(image)

    text = pytesseract.image_to_string(Image.fromarray(processed_image))
    return text.strip()

def analyze_prescription(text):
    """Analyze extracted text and suggest tests & doctors"""
    suggestions = {"tests": [], "doctors": []}

    # Example Keywords for Tests
    test_keywords = {
        "blood test": ["CBC", "Complete Blood Count", "Hemoglobin"],
        "diabetes": ["Blood Sugar", "Glucose Test"],
        "cholesterol": ["Lipid Profile", "Cholesterol Test"],
        "thyroid": ["TSH", "Thyroid Function Test"],
    }

    # Example Keywords for Specialists
    doctor_keywords = {
        "cardiologist": ["heart", "ECG", "hypertension"],
        "endocrinologist": ["thyroid", "diabetes", "hormone"],
        "neurologist": ["migraine", "seizure", "brain"],
    }

    # Find matching tests
    for test, keywords in test_keywords.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            suggestions["tests"].append(test)

    # Find matching specialists
    for doctor, keywords in doctor_keywords.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            suggestions["doctors"].append(doctor)

    return suggestions
