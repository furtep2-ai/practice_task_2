from database import engine
from models import Base, Note
import asyncio
from database import AsyncSessionLocal
from sqlalchemy import delete

async def database_create():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def insert_data():
    async with AsyncSessionLocal() as session:
        note = Note(text = "План встречи" , version = 1)
        session.add(note)
        await session.commit()

async def delete_data():
    async with AsyncSessionLocal() as session:
        result = await session.execute(delete(Note).where(Note.id == 1))
        await session.commit()
        if result.rowcount == 1:
            print("Усепх")
        

asyncio.run(insert_data())
