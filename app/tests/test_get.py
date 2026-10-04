import pytest
from app.models import Note
from sqlalchemy import delete

@pytest.mark.asyncio
@pytest.mark.parametrize("note, status_code", [
    (True, 200),
    (False, 404)
])
async def test_success_get(client, db_session_factory, note, status_code):
    if not note:
        async with db_session_factory() as db:
            await db.execute(delete(Note).where(Note.id == 1))
            await db.commit()

    response = await client.get("/notes/1")
    data = response.json()

    assert response.status_code == status_code

    if note:
        assert data["id"] == 1
        assert data["text"] == "План встречи"
        assert data["version"] == 1
    else:
        assert data["detail"] == "Not found note"


        





