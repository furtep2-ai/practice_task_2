from app.main import app, get_db
import pytest
from app.models import Note


@pytest.mark.asyncio
async def test_success_changing(client):
    result = await client.patch("/notes/1", 
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={"text": "Новый текст", "version": 1}
    )
    assert result.status_code==200
    data = result.json()
    assert data["text"] == "Новый текст"
    assert data["version"] == 2

@pytest.mark.asyncio
async def test_uncorrect_version(client):
    result = await client.patch("/notes/1", 
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={"text": "Новый текст", "version": 1}
    )

    assert result.status_code==200
    data = result.json()
    assert data["text"] == "Новый текст"
    assert data["version"] == 2

    result = await client.patch("/notes/1", 
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={"text": "dsd", "version": 1}
    )
    assert result.status_code==409
    data = result.json()
    assert "detail" in data
    assert data["detail"] == f"Version conflict, current_version:{2}"

@pytest.mark.asyncio
@pytest.mark.parametrize("text, version", [
    ("", 1),
    ("    ", 1)
])
async def test_empty_text(client, text, version):
    result = await client.patch("/notes/1", 
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={"text": text, "version": version}
    )
    assert result.status_code==422

@pytest.mark.asyncio
async def test_not_note(client):
    result = await client.patch("/notes/99", 
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={"text": "Новый текст", "version": 1}
    )
    assert result.status_code==404
    data = result.json()
    assert "detail" in data
    assert data["detail"] == "Not found note"
    


