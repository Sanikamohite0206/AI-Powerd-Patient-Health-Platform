from flask import Flask
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from config import Config
from routes.file_routes import file_bp
from routes.ocr_routes import ocr_bp
from routes.chatbot_routes import chatbot_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"])

app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY

jwt = JWTManager(app)

# ✅ Fixed Blueprint Registration
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(file_bp, url_prefix="/api/files")
app.register_blueprint(ocr_bp, url_prefix="/api/ocr")
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")

if __name__ == "__main__":
    app.run(debug=True)
