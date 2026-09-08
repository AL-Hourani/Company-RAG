
import asyncio
from sqlalchemy import text
from app.database.session import AsyncSessionLocal

async def main() -> None:
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT 1")
        )
        
        value = result.scalar_one()

        print(f"Database connection OK: {value}")

if __name__ == "__main__":
    asyncio.run(main())