from datetime import datetime

class File:
    def __init__(self, user_email, file_url, file_type):
        self.user_email = user_email
        self.file_url = file_url
        self.file_type = file_type
        self.uploaded_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_email": self.user_email,
            "file_url": self.file_url,
            "file_type": self.file_type,
            "uploaded_at": self.uploaded_at
        }
