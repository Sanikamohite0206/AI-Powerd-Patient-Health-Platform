import google.generativeai as genai
from config import Config

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)

def get_gemini_explanation(ocr_text):
    """Use Gemini AI to explain the extracted text"""
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Explain this medical prescription text in simple words for a patient: {ocr_text}"
    
    response = model.generate_content(prompt)
    
    return response.text if response else "Unable to generate an explanation."
