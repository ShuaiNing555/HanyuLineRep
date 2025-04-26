import pytest
from fastapi.testclient import TestClient
from api import app 
from data import DataManager
from database import init_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    init_db()
    yield

def test_add_word(setup_database):
    response = client.post("/words", json={"word": "тест", "transcription": "[tɛst]", "translation": "тест"})
    assert response.status_code == 200
    assert response.json() == {"word": "тест", "transcription": "[tɛst]", "translation": "тест"}

def test_get_words(setup_database):
    response = client.get("/words")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_random_word(setup_database):
    response = client.post("/words", json={"word": "слово", "transcription": "[slovo]", "translation": "слово"})
    assert response.status_code == 200

    response = client.get("/random_word")
    assert response.status_code == 200
    assert "слово" in response.text

def test_view_unknown_words(setup_database):
    response = client.get("/unknown_words")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_unknown_word(setup_database):
    response = client.post("/unknown_words", json={"user_id": 1, "word": "незнакомое"})
    assert response.status_code == 200
    assert response.json() == {"message": "Слово 'незнакомое' добавлено."}