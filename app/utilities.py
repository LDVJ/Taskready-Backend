from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from .config import settings
import uuid
import logging
import resend

hashing  = PasswordHash.recommended()
resend.api_key = settings.EMAIL_API_KEY 

# password
def create_hash_password(plain_password: str) -> str:
    return hashing.hash(password=plain_password)

def verify_hash_password(plain_password :str, hashed_password: str) -> bool:
    return hashing.verify(password=plain_password,hash= hashed_password)

#jwt session 

def create_access_token(user_data: dict, expire_at : timedelta = timedelta(minutes=30), refres : bool = None):
    payload = {
        "user" : user_data,
        "exp": datetime.now(timezone.utc) + expire_at,
        "jti": str(uuid.uuid4())
    }

    access_token = jwt.encode(algorithm=settings.ALGORITHM, key=settings.SECRET_KEY, payload=payload)

    return access_token

def decode_access_token(token : str):
    try:
        user = jwt.decode(jwt=token, algorithms=[settings.ALGORITHM], key=settings.SECRET_KEY)
        return user
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

# email token

def create_verification_token(email: str) -> str:
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode = {
        "sub":email,
        "exp":expire_at
    }
    token = jwt.encode(to_encode, key=settings.EMAIL_API_KEY, algorithm=settings.ALGORITHM)
    return token

def send_verification_email(email: str, token: str, name: str):
    verify_url = f'{settings.DOMAIN_NAME}/users/verify?token={token}'
    # print("verify_url",verify_url)
    print(f"--- DEBUG: Attempting to send email with API Key: '{resend.api_key}' ---")

    params = {
        "from": "onboarding@resend.dev", # Verified domain required for custom emails
        "to": email,
        "subject": "Verify your Taskready Account",
        "html": f"""
            <h3>Hi {name},</h3>
            <p>Thanks for signing up! Please verify your email by clicking the link below:</p>
            <a href="{verify_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Verify Email Address
            </a>
            <p>If the button doesn't work, copy this link: {verify_url}</p>
        """
    }
    print("params",params)
    
    try:
        resend.Emails.send(params=params)
    except Exception as e:
        print(f'Resend Error: {e}')