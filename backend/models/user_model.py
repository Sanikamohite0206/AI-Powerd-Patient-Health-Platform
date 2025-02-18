import bcrypt

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def to_dict(self):
        return {"email": self.email, "password": self.password}

    @staticmethod
    def check_password(stored_password, input_password):
        return bcrypt.checkpw(input_password.encode("utf-8"), stored_password.encode("utf-8"))
