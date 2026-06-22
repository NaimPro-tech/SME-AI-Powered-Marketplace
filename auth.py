from fastapi import APIRouter, HTTPException, status, Depends
from database import database
from schemas import UserCreate, UserResponse, UserLogin, PasswordUpdate, ResetPassword, ForgetPasswordRequest
from security import create_access_token, get_current_user, create_password_reset_token, verify_password_reset_token
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt

#create authentication router
router = APIRouter(prefix="/auth", tags=["Authentication"])

#hashing function
def get_password_hash(password: str)->str:
    #convert pass string into byte
    pwd_bytes = password.encode('utf-8')
    #generate salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt=salt)
    #create string to return text into database
    return hashed_password.decode('utf-8')

#password matching function
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


#user Registration endpoint
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    #check email if already have or not
    query = "SELECT * FROM users WHERE email = :email"
    existing_user = await database.fetch_one(query=query, values={"email":user.email})

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "Already created an account with this email."
        )
    
    #hashing password
    hashed_password = get_password_hash(user.password)

    #insert new user to the database
    insert_query = """INSERT INTO users(name, email, password, role)
                    VALUES (:name, :email, :password, :role)
                    RETURNING user_id, name, email, role
    """

    new_user = await database.fetch_one(
        query=insert_query,
        values={
            "name":user.name,
            "email":user.email,
            "password":hashed_password,
            "role":user.role
        }
    )
    return new_user

#user login endpoint
@router.post("/login")
async def login_user(user: OAuth2PasswordRequestForm = Depends()):
    #search user in database
    query = "SELECT * FROM users WHERE email=:email"
    db_user = await database.fetch_one(query=query, values={"email":user.username})

    #verify_password will match password directly with bcrypt
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong Username or Password"
        )
    
    #jwt token creation if login credentials will match
    #we put user id, email and role into payload
    token_data = {
        "user_id":db_user["user_id"],
        "email":db_user["email"],
        "role":db_user["role"]
    }

    access_token = create_access_token(data=token_data)

    #send token to frontend
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

#update new password with old password for loged in users
@router.put("/update-password", status_code=status.HTTP_200_OK)
async def update_password(data: PasswordUpdate, curren_user: dict = Depends(get_current_user)):
    query = "SELECT password FROM users WHERE user_id = :user_id"
    db_user = await database.fetch_one(query=query, values={"user_id": curren_user["user_id"]})

    #check if old password match or not
    if not verify_password(data.old_password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password does not match."
        )
    #update new hashed password
    new_hash_password = get_password_hash(data.new_password)
    update_query = "UPDATE users SET password = :password WHERE user_id = :user_id"

    await database.execute(update_query, values={"password": new_hash_password, "user_id":curren_user["user_id"]})

    return {"message":"Password updated successfully."}

#forget password request(link/token generate)
@router.post("/forget-password", status_code=status.HTTP_200_OK)
async def forget_password(data: ForgetPasswordRequest):
    query = "SELECT  email FROM users WHERE email = :email"
    user = await database.fetch_one(query=query, values={"email":data.email})

    if not user:
        #for security purpose used generic message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist"
        )
    
    #create reset token
    reset_token = create_password_reset_token(data.email)

    #in production we have sent link in user email with fastapio-mail or any SMTP
    #for now we send token into response for testing
    return {
        "message": "Password reset token generated. In production, this will be sent via email.",
        "reset_token": reset_token
    }

#new password update with token from email
@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetPassword):
    #check if token is valid or not
    email = verify_password_reset_token(data.token)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or Expired Token."
        )
    
    new_hashed_password = get_password_hash(data.new_password)

    #update password in database
    update_query = "UPDATE users SET password = :password WHERE email = :email"
    await database.execute(query=update_query, values={"password": new_hashed_password, "email": email})

    return {"message": "Password has been reset successfully. You can now login with your new password"}