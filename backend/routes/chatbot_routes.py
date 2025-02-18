from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.database import db
from utils.gemini_helper import get_gemini_explanation

chatbot_bp = Blueprint("chatbot_bp", __name__)

@chatbot_bp.route("/explain", methods=["POST"])
@jwt_required()
def explain_ocr_results():
    """AI chatbot to explain OCR results"""
    data = request.json
    file_url = data.get("file_url")

    if not file_url:
        return jsonify({"message": "File URL is required"}), 400

    # Retrieve OCR result from database
    user_email = get_jwt_identity()
    ocr_result = db.ocr_results.find_one({"user_email": user_email, "file_url": file_url})

    if not ocr_result:
        return jsonify({"message": "No OCR result found for this file"}), 404

    extracted_text = ocr_result["extracted_text"]

    # Get AI explanation from Gemini
    explanation = get_gemini_explanation(extracted_text)

    return jsonify({
        "message": "AI Explanation Generated",
        "extracted_text": extracted_text,
        "explanation": explanation
    }), 200
