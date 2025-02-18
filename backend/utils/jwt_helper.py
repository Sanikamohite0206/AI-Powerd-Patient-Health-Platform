from flask_jwt_extended import create_access_token
from datetime import timedelta

def generate_token(email):
    return create_access_token(identity=email, expires_delta=timedelta(days=1))
