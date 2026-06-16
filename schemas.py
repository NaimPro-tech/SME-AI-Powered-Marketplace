from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

#user registration data
class UserCreate(BaseModel):
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

# to create pydantic schemas for product
class ProductCreate(BaseModel):
    title:str
    description:Optional[str]=None
    base_price: float
    discount_price:Optional[float]=0.00
    is_offer_active:Optional[bool]=False
    category:Optional[str]=None

#return fields when it get back from database
class ProductResponse(BaseModel):
    product_id: int
    title: str
    description:Optional[str]
    base_price:float
    discount_price:float
    seller_id:int
    is_offer_active:bool
    category:Optional[str]
    view_count:int
    sales_count:int
    created_at:datetime

    class Config:
        from_attributes = True