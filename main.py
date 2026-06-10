from fastapi import FastAPI
from auth import router as auth_router
from database import database

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