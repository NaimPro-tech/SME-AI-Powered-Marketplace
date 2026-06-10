import asyncio
from databases import Database

# ডাটাবেজ কানেকশন ইউআরএল (আপনার পাসওয়ার্ডটি এখানে বসান)
# ফরম্যাট: postgresql://ইউজারনেম:পাসওয়ার্ড@হোস্ট:পোর্ট/ডাটাবেজের_নাম

DB_URL = "postgresql://postgres:NPro009@@localhost:5432/ai_marketplace"

#create database with database library

database = Database(DB_URL)

async def test_connection():
    print("Trying to connect with database...")

    try:
        await database.connect()
        print("Successfully connected to database.")

        #test with a simple query
        query = "SELECT version()"
        version = await database.fetch_val(query=query)
        print(f"Poestgre Version: {version}")

    except Exception as e:
        print(f"Failed to connect database: {e}")

    finally:
        await database.disconnect()

if __name__ == "__main__":
    asyncio.run(test_connection())