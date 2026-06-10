from pydantic import BaseModel, EmailStr
from typing import Optional

#user registration data
class UsearCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:Optional[str] = 'buyer'

#user login model
class UserLogin(BaseModel):
    email:EmailStr
    password:str

#response that will send to user(password will be hidden for security)
class UserResponse(BaseModel):
    user_id:int
    name:str
    email:EmailStr
    role:str

    class config:
        from_attributes = True