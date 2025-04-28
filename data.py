import random
from sqlalchemy.future import select
from models import Word, Text

class DataManager:
    def __init__(self):
        self.words = []  
        self.texts = [] 
        self.used_words = [] 

    async def load_words_from_db(self, session):
        result = await session.execute(select(Word))
        self.words = result.scalars().all() 

    async def load_texts_from_db(self, session):
        result = await session.execute(select(Text))
        self.texts = result.scalars().all() 

    def get_random_text(self):
        return random.choice(self.texts) if self.texts else None

    def get_random_word(self):
        available_words = [word for word in self.words if word not in self.used_words]
        if available_words:
            random_word = random.choice(available_words)
            self.used_words.append(random_word) 
            return random_word  
        return None