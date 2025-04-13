import random
from models import Word
from sqlalchemy.future import select

class DataManager:
    def __init__(self):
        self.texts = [{"我要去北京旅游，你觉得什么时候去最好？九月去北京旅游最好。为什么？九月的北京天气不冷也不热。"},
    {"你喜欢什么运动？我最喜欢踢足球。下午我们一起去踢足球吧。好啊！"}]
        self.known_words = [] 
        self.words = [{"word": "要", "transciption": "[yào]", "translation": "[хотеть]"},
    {"word": "旅游", "transciption": "[lǚyóu]","translation": "[путешествовать]"},
    {"word": "觉得", "transciption": "[juéde]","translation": "[думать]"},
    {"word": "时候", "transciption": "[shíhou]","translation": "[время]"},
    {"word": "最", "transciption": "[zuì]","translation": "[больше всего]"},
    {"word": "冷", "transciption": "[lěng]","translation": "[холодный]"},
    {"word": "热", "transciption": "[rè]","translation": "[горячий]"},
    {"word": "运动","transciption": "[yùndòng]", "translation": "[заниматься спортом]"},
    {"word": "下午", "transciption": "[xiàwǔ]","translation": "[после обеда]"}]  

    def get_texts(self):
        return self.texts

    def get_random_text(self):
        return random.choice(self.texts) if self.texts else None

    def get_words_from_text(self, text):
        return text.split()  

    def add_unknown_word(self, word):
        if word not in self.known_words:
            self.known_words.append(word)

    def get_known_words(self):
        return self.known_words

    def get_random_word(self):
        return random.choice(self.words) if self.words else None

    async def load_words_from_db(self, session):
        result = await session.execute(select(Word))
        self.words = [{"word": word.word, "transcription": "", "translation": word.translation} for word in result.scalars().all()]
        self.known_words = self.words

    async def add_word_to_db(self, session, word, translation):
        new_word = Word(word=word, translation=translation)
        session.add(new_word)
        await session.commit()

data_manager = DataManager()