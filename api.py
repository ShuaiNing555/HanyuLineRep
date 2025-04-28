from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db, init_db
from models import Word, Text
from pydantic import BaseModel
from typing import List
import random
from contextlib import asynccontextmanager

class WordResponse(BaseModel):
    word: str
    transcription: str
    translation: str

class TextResponse(BaseModel):
    content: str

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db() 
    yield 

app = FastAPI(lifespan=lifespan)

@app.get("/words/random", response_model=WordResponse)
async def get_random_word(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Word))
    words = result.scalars().all()
    if words:
        random_word = random.choice(words)
        return WordResponse(word=random_word.word, transcription=random_word.transcription, translation=random_word.translation)
    raise HTTPException(status_code=404, detail="No words found")

@app.get("/texts/random", response_model=TextResponse)
async def get_random_text(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Text))
    texts = result.scalars().all()
    if texts:
        random_text = random.choice(texts)
        return TextResponse(content=random_text.content)
    raise HTTPException(status_code=404, detail="No texts found")

@app.get("/words", response_model=List[WordResponse])
async def get_words(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Word))
    words = result.scalars().all()
    return [WordResponse(word=w.word, transcription=w.transcription, translation=w.translation) for w in words]

@app.get("/texts", response_model=List[TextResponse])
async def get_texts(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Text))
    texts = result.scalars().all()
    return [TextResponse(content=t.content) for t in texts]

@app.post("/words", response_model=WordResponse)
async def add_word(word: WordResponse, session: AsyncSession = Depends(get_db)):
    new_word = Word(user_id=1, word=word.word, translation=word.translation)
    session.add(new_word)
    await session.commit()
    await session.refresh(new_word)
    return WordResponse(word=new_word.word, transcription=new_word.transcription, translation=new_word.translation)

@app.post("/texts", response_model=TextResponse)
async def add_text(text: TextResponse, session: AsyncSession = Depends(get_db)):
    new_text = Text(content=text.content)
    session.add(new_text)
    await session.commit()
    await session.refresh(new_text)
    return TextResponse(content=new_text.content)