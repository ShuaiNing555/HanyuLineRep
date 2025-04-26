from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import get_db
from data import DataManager

app = FastAPI()
data_manager = DataManager()

class WordModel(BaseModel):
    word: str
    transcription: str
    translation: str

class TextModel(BaseModel):
    text: str

@app.get("/words", response_model=List[WordModel])
async def get_words():
    return data_manager.get_known_words()

@app.post("/words", response_model=WordModel)
async def add_word(word: WordModel):
    async with get_db() as session:
        await data_manager.add_word_to_db(session, word.word, word.translation)
    return word

@app.get("/texts", response_model=List[TextModel])
async def get_texts():
    async with get_db() as session:
        await data_manager.load_texts_from_db(session)
        return data_manager.texts

@app.post("/texts", response_model=TextModel)
async def add_text(text: TextModel):
    async with get_db() as session:
        await data_manager.add_text_to_db(session, text.text)
    return text