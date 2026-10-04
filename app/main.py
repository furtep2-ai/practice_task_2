from app.database import AsyncSessionLocal, AsyncSession
from app.models import Note
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, update
from pydantic import BaseModel, StringConstraints, Field
from typing import Annotated

app = FastAPI()

class NoteChange(BaseModel):
    text: Annotated[str, StringConstraints(min_length=1, max_length=200, strip_whitespace=True)]
    version: Annotated[int, Field(gt=0)]

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/notes/{note_id}")
async def get_notes(note_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Note).where(Note.id == note_id))
    note = result.scalar_one_or_none()
    

    if not note:
        raise HTTPException(status_code = 404, detail = "Not found note")

    return {"id": note.id, "text": note.text.strip(), "version": note.version}

@app.patch("/notes/{note_id}")
async def change_notes(note_id: int, payloads: NoteChange, session: AsyncSession = Depends(get_db)):
    change = (
        update(Note)
        .where(Note.id == note_id, Note.version == payloads.version)
        .values(text=payloads.text, version=payloads.version+1)
        .returning(Note)
    )

    result = await session.execute(change)
    update_note = result.scalar_one_or_none()
    await session.commit()

    if update_note:
        return {"text": update_note.text, "version": update_note.version}

    query = await session.execute(select(Note).where(Note.id == note_id))
    note = query.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code = 404, detail="Not found note") 
    
    raise HTTPException(status_code = 409, detail=f"Version conflict, current_version:{note.version}")





    


    

