import cloudinary
import cloudinary.uploader
from config import Config

# Configure Cloudinary
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)

def upload_to_cloudinary(file):
    try:
        result = cloudinary.uploader.upload(file)

        if "secure_url" in result:
            return result["secure_url"]
        else:
            print("❌ Cloudinary Upload Error: No secure_url returned.")
            return None

    except Exception as e:
        print(f"❌ Cloudinary Upload Failed: {e}")
        return None
