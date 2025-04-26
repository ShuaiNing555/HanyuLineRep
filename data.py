import random
from models import Word, Text 
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

class DataManager:
    def __init__(self):
        self.known_words = []  
        self.words = []  
        self.used_words = []  
        self.unknown_words = {}  
        self.texts = []  

    async def load_words_from_db(self, session: AsyncSession):
        result = await session.execute(select(Word))
        self.words = [{"word": row.word, "transcription": row.transcription, "translation": row.translation} for row in result.scalars()]

    async def load_texts_from_db(self, session: AsyncSession):
        result = await session.execute(select(Text))
        self.texts = [{"text": row.text} for row in result.scalars()]

    async def add_text_to_db(self, session: AsyncSession, text: str):
        new_text = Text(text=text)
        session.add(new_text)
        await session.commit()

    def get_random_text(self):
        return random.choice(self.texts) if self.texts else None

    def add_unknown_word(self, user_id, word):
        if user_id not in self.unknown_words:
            self.unknown_words[user_id] = []
        self.unknown_words[user_id].append(word)

    def get_unknown_words(self, user_id):
        return self.unknown_words.get(user_id, [])

    def get_known_words(self):
        return [word['word'] for word in self.known_words]  

    def get_random_word(self):
        available_words = [word for word in self.words if word not in self.used_words]
        if available_words:
            random_word = random.choice(available_words)
            self.used_words.append(random_word)
            return random_word  
        return None  

    async def add_word_to_db(self, session: AsyncSession, word: str, translation: str):
        new_word = Word(word=word, translation=translation)
        session.add(new_word)
        await session.commit()
        self.known_words.append({"word": word, "translation": translation})