from pwdlib import PasswordHash
import jwt
from fastapi import HTTPException, status
from .config import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime, timedelta, timezone
from fastapi.security import oauth2
from .config import settings
import hashlib
import secrets

hashing  = PasswordHash.recommended()
# resend.api_key = settings.EMAIL_API_KEY_RESEND
sg_client= SendGridAPIClient(settings.SENDGRID_API_KEY)

OAuth2_schema = oauth2.OAuth2PasswordBearer(tokenUrl="login")


# password
def create_hash_password(plain_password: str) -> str:
    return hashing.hash(password=plain_password)

def verify_hash_password(plain_password :str, hashed_password: str) -> bool:
    return hashing.verify(password=plain_password,hash= hashed_password)


# email token

def create_verification_token(email: str) -> str:
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode = {
        "sub":email,
        "exp":expire_at
    }
    token = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def send_verification_email(email: str, token: str, name: str):
    verify_url = f'{settings.DOMAIN_NAME}/users/verify?token={token}'
    brand_orange = "#E87722"
    brand_navy = "#1D3557"
    off_white = "#FDF8EE"

    html_content = f"""
    <div style="background-color: {off_white}; padding: 50px 20px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; text-align: center;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 10px solid {brand_orange};">
            <div style="padding: 40px 30px;">
                <!-- Logo Text -->
                <h1 style="color: {brand_navy}; margin: 0 0 10px 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; font-weight: 900;">
                    TASK READY
                </h1>
                
                <h2 style="color: {brand_navy}; margin-bottom: 20px; font-size: 22px;">Confirm Your Email</h2>
                
                <p style="color: #555555; font-size: 16px; line-height: 1.6; margin-bottom: 30px;">
                    Hi <strong>{name}</strong>,<br>
                    Welcome to Task Ready! To get started, please verify your email address by clicking the button below.
                </p>

                <!-- Centralized Button -->
                <div style="margin: 35px 0;">
                    <a href="{verify_url}" style="background-color: {brand_orange}; color: #ffffff; padding: 16px 35px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; display: inline-block; box-shadow: 0 4px 6px rgba(232, 119, 34, 0.3);">
                        VERIFY EMAIL ADDRESS
                    </a>
                </div>

                <p style="color: #888888; font-size: 13px; margin-top: 40px;">
                    If the button doesn't work, copy and paste this link into your browser:
                </p>
                <p style="word-break: break-all; margin-top: 10px;">
                    <a href="{verify_url}" style="color: {brand_navy}; font-size: 12px; text-decoration: underline;">{verify_url}</a>
                </p>
            </div>
            
            <div style="background-color: #f9f9f9; padding: 20px; border-top: 1px solid #eeeeee;">
                <p style="color: #aaaaaa; font-size: 11px; margin: 0;">
                    &copy; 2024 Task Ready Inc. All rights reserved.
                </p>
            </div>
        </div>
    </div>
    """
    message = Mail(

        from_email=settings.SENDGRID_EMAIL, 
        to_emails=email,
        subject='Verify your Taskready Account',
        html_content=html_content
    )
    
    try:
        sg_client.send(message)
    except Exception as e:
        print(f'SendGrid Error: {e}')


def  verify_verification_email(token: str):
    try:
        user_info = jwt.decode(token, algorithms=[settings.ALGORITHM], key=settings.SECRET_KEY)
        return user_info
    except jwt.ExpiredSignatureError:
        # Specific PyJWT exception for expired tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="The verification link has expired."
        )
    except jwt.InvalidTokenError:
        # Catch-all for any other JWT issues (invalid signature, malformed, etc.)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or tampered verification link."
        )
    

def hash_refresh_token(token : str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def verify_hash_token(token :str, hash_token_db :str) -> bool:
    hashed_token = hash_refresh_token(token)
    return secrets.compare_digest(hashed_token, hash_token_db)