import asyncio
from database import engine, initialize_database
from sqlalchemy import text

async def test_connection():
    try:
        async with engine.begin() as conn:
            print("Connecting to the database...")
            await conn.execute(text("SELECT 1"))
            print("Database connection successful.")

            await initialize_database()
    except Exception as e:
        print(f"Error while connecting to database:\n{e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())