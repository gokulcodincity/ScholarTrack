import logging
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"

# Configure logging to show email output in the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_verification_token(email: str):
    """Generate a JWT token for email verification valid for 24 hours."""
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def send_verification_email(email: str, name: str):
    """
    Mock email sender.
    In production, this would use an SMTP server like SendGrid or AWS SES.
    """
    token = create_verification_token(email)
    
    # URL pointing to our new Frontend verify page
    verification_url = f"http://localhost:5173/verify-email?token={token}"
    
    email_content = f"""
    ================================================================
    NEW EMAIL OUTBOUND:
    To: {email}
    Subject: ScholarTrack - Please Verify Your Email
    
    Hello {name},
    
    Welcome to ScholarTrack! To complete your registration and log in, 
    please click the link below to verify your email address:
    
    {verification_url}
    
    This link will expire in 24 hours.
    ================================================================
    """
    
    # Print the "email" to the server terminal using print() to bypass JSON loggers
    print("\n" + email_content + "\n", flush=True)
