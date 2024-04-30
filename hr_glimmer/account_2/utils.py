# utils.py
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt=settings.SECRET_KEY)

def verify_token(token, max_age=3600):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=settings.SECRET_KEY, max_age=max_age)
        return email
    except Exception as e:
        return None
