from fastapi import FastAPI, Depends
from database import database
from security import get_current_user

app = FastAPI(
    title="AI-Powered Dynamic Marketplace API",
    description="Intelligent Insight, Bidding System, Competitor Analysis Platform",
    version="1.0.0"
)

#database will connect starting on application

@app.on_event("startup")
async def startup():
    await database.connect()
    print("Database Connected Successfully.")

#database will close with application closing
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    print("Successfully Disconnected")

#basic home route(root endpoint)
@app.get("/")
def home():
    return {
        "message":"Welcome to AI-Powered Dynamic Marketplace.",
        "status":'Running',
        'features':[
            "AI Sales Prediction",
            "Competitor Web Scrapping",
            "Buyer Recomendations",
            "Bidding System"
        ]
    }

@app.get("/users/me")
async def get_my_profile(current_user: dict=Depends(get_current_user)):
    """This router is completely secure
        without token it will hit 401 error"""
    return {
        "message": "Welcome to Dashboard",
        "user_details": current_user
    }