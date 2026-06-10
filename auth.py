from fastapi import APIRouter, HTTPException, status
from database import database
from schemas import UsearCreate, UserResponse, UserLogin
# from passlib.context import CryptContext
import bcrypt

# #create context for password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
async def register_user(user: UsearCreate):
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
async def login_user(user: UserLogin):
    #search user in database
    query = "SELECT * FROM users WHERE email=:email"
    db_user = await database.fetch_one(query=query, values={"email":user.email})

    #verify_password will match password directly with bcrypt
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong Username or Password"
        )
    
    return {
        "message":"Login Successfull",
        "user":{
            "id":db_user['user_id'],
            "name":db_user['name'],
            "email":db_user['email'],
            "role":db_user['role']
        }
    }