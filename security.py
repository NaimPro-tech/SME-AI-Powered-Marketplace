from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
import os
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

#load variable from .env file
load_dotenv()


#collect values from .env file
#if somehow value missing in .env then the 2nd parameter will work as backup
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_super_secret_key_for_local_only")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))

def create_access_token(data: dict):
    """secure jwt creation function"""

    to_encode = data.copy()

    #token expire time
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    #add expire time into payload
    to_encode.update({"exp":expire})

    #token encode/generate
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#path where frontend/porstman will get the token 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str=Depends(oauth2_scheme)):
    """this function will take token from request header.
        and will decode with secret_key then it will return info of user"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or Expired Token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        #break the token to get insider(payload) information
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")
        role: str = payload.get("role")

        #if token is blank
        if user_id or email is None:
            raise credentials_exception
        
        return {"user_id":user_id, "email":email, "role":role}
    
    except jwt.ExpiredSignatureError:
        #after 30 mins of token generation
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session Expired."
        )
    except jwt.PyJWTError:
        #if anyone try to rewrite or give fraud token
        raise credentials_exception
    