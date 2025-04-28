import pytest
from fastapi.testclient import TestClient
from api import app
from database import init_db, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models import Word, Text

client = TestClient(app)

@pytest.fixture(scope="module")
async def setup_database():
    await init_db()
    yield

@pytest.fixture(scope="module")
async def test_db(setup_database):
    async with get_db() as session:
        word1 = Word(user_id=1, word="тест", translation="test")
        word2 = Word(user_id=1, word="пример", translation="example")
        session.add(word1)
        session.add(word2)
        await session.commit()

        text1 = Text(content="Это тестовый текст.")
        text2 = Text(content="Это еще один текст.")
        session.add(text1)
        session.add(text2)
        await session.commit()

        yield session

@pytest.mark.asyncio
async def test_get_random_word(test_db):
    response = client.get("/words/random")
    assert response.status_code == 200
    assert "word" in response.json()
    assert "translation" in response.json()

@pytest.mark.asyncio
async def test_get_words(test_db):
    response = client.get("/words")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  

@pytest.mark.asyncio
async def test_get_random_text(test_db):
    response = client.get("/texts/random")
    assert response.status_code == 200
    assert "content" in response.json()

@pytest.mark.asyncio
async def test_get_texts(test_db):
    response = client.get("/texts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  

@pytest.mark.asyncio
async def test_add_word(test_db):
    response = client.post("/words", json={"word": "новое слово", "transcription": "[novoe slovo]", "translation": "new word"})
    assert response.status_code == 200
    assert response.json()["word"] == "новое слово"

@pytest.mark.asyncio
async def test_add_text(test_db):
    response = client.post("/texts", json={"content": "Новый текст для тестирования."})
    assert response.status_code == 200
    assert response.json()["content"] == "Новый текст для тестирования."