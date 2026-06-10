from fastapi import FastAPI
from database import database

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