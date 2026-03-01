from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from .config import settings
import uuid
import logging
import resend

hashing  = PasswordHash.recommended()

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
        "email":email,
        "exp":expire_at
    }
    return jwt.encode(to_encode, algorithm=[settings.ALGORITHM], key=settings.VERIFICATION_SECRET_KEY)

def send_verification_email(email: str, token: str):
    verify_url = f''