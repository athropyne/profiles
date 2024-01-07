from sqlalchemy.ext.asyncio import create_async_engine

from config import DB_URL

engine = create_async_engine(f"{DB_URL}/profiles", echo=True)


async def get_connection():
    async with engine.connect() as connection:
        yield connection
        await connection.commit()
