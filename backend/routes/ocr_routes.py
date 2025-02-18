from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.database import db
from utils.ocr_helper import extract_text_from_image, analyze_prescription

ocr_bp = Blueprint("ocr_bp", __name__)

@ocr_bp.route("/process", methods=["POST"])
@jwt_required()
def process_uploaded_file():
    """Process an uploaded image for OCR and analyze prescriptions"""
    data = request.json
    file_url = data.get("file_url")

    if not file_url:
        return jsonify({"message": "File URL is required"}), 400

    # Extract text from image
    extracted_text = extract_text_from_image(file_url)

    # Analyze prescription and suggest tests & doctors
    suggestions = analyze_prescription(extracted_text)

    # Store analysis in MongoDB
    user_email = get_jwt_identity()
    db.ocr_results.insert_one({
        "user_email": user_email,
        "file_url": file_url,
        "extracted_text": extracted_text,
        "suggestions": suggestions
    })

    return jsonify({
        "message": "OCR processing completed",
        "extracted_text": extracted_text,
        "suggestions": suggestions
    }), 200
