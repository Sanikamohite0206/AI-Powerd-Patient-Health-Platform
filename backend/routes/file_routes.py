from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.cloudinary_helper import upload_to_cloudinary
from db.database import db
from models.file_model import File

file_bp = Blueprint("file_bp", __name__)

@file_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file provided"}), 400

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    file_url = upload_to_cloudinary(file)
    file_type = file.content_type

    if not file_url:
        return jsonify({"message": "File upload failed"}), 500

    user_email = get_jwt_identity()

    file_entry = File(user_email, file_url, file_type)
    db.uploaded_files.insert_one(file_entry.to_dict())

    return jsonify({"message": "File uploaded successfully", "file_url": file_url}), 201
