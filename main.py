from fastapi import FastAPI, Depends
from auth import router as auth_router
from database import database
from security import get_current_user

app = FastAPI(
    title="AI-Powered Dynamic Marketplace API",
    description="Intelligent Insight, Bidding System and Competitor Analysis Platform",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    await database.connect()
    print("Database Connected Successfully.")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    print("Connection has been Shutdown.")

#auth_router connect to the app
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message":"AI-Powered Dynamic Marketplace.",
        "status":"running"
    }
#test the lock
@app.get("/users/me")
async def get_my_profile(current_user: dict=Depends(get_current_user)):
    """This router is completely secure
        without token it will hit 401 error"""
    return {
        "message": "Welcome to Dashboard",
        "user_details": current_user
    }