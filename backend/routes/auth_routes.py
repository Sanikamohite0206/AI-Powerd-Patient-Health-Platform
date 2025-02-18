from flask import Blueprint, request, jsonify
from db.database import users_collection
from models.user_model import User
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    user = User(email, password)
    users_collection.insert_one(user.to_dict())

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})

    if not user or not User.check_password(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({"access_token": access_token}), 200

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"message": "Access granted to protected route"}), 200

@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    print(f"🔍 Headers Received: {request.headers}")  # Debugging
    print(f"🔍 Authorization Header: {request.headers.get('Authorization')}")  # Debugging

    user_email = get_jwt_identity()
    if not user_email:
        return jsonify({"message": "Invalid token"}), 401  # ✅ Return proper error

    return jsonify({"user": {"name": "Test User", "email": user_email}}), 200