import random
from models import Word  
from sqlalchemy.future import select

class DataManager:
    def __init__(self):
        self.texts = [
            {"text": "我要去北京旅游，你觉得什么时候去最好？九月去北京旅游最好。"},
            {"text": "你很少生病，是不是喜欢运动？是啊，我每天早上都要出去跑步。你每天几点起床？我每天六点起床。"},
            {"text": "吃药了吗？现在身体怎么样？吃了。现在好多了。"},
            {"text": "大卫今年多大？二十多岁。他多高？一米八几。"},
            {"text": "张老师星期六也不休息啊？是啊，他这几天很忙，没有时间休息。"}
        ]

        self.known_words = []  
        self.words = []  
        self.used_words = []  
        self.unknown_words = {}  

    async def load_words_from_db(self, session):
        result = await session.execute(select(Word))
        db_words = [
            {"word": "要", "transcription": "[yào]", "translation": "[хотеть]"},
            {"word": "旅游", "transcription": "[lǚyóu]", "translation": "[путешествовать]"},
            {"word": "觉得", "transcription": "[juéde]", "translation": "[думать]"},
            {"word": "时候", "transcription": "[shíhou]", "translation": "[время]"},
            {"word": "最", "transcription": "[zuì]", "translation": "[больше всего]"},
            {"word": "冷", "transcription": "[lěng]", "translation": "[холодный]"},
            {"word": "热", "transcription": "[rè]", "translation": "[горячий]"},
            {"word": "运动", "transcription": "[yùndòng]", "translation": "[заниматься спортом]"},
            {"word": "下午", "transcription": "[xiàwǔ]", "translation": "[после обеда]"}
        ] 
        if db_words:
            self.words = db_words 
            self.known_words = self.words  

    def add_unknown_word(self, user_id, word):
        if user_id not in self.unknown_words:
            self.unknown_words[user_id] = []
        self.unknown_words[user_id].append(word)

    def get_unknown_words(self, user_id):
        return self.unknown_words.get(user_id, [])

    def get_known_words(self):
        return [word['word'] for word in self.known_words]  

    def get_random_text(self):
        return random.choice(self.texts) if self.texts else None

    def get_random_word(self):
        available_words = [word for word in self.words if word not in self.used_words]
        if available_words:
            random_word = random.choice(available_words)
            self.used_words.append(random_word)
            return random_word  
        return None  

    async def add_word_to_db(self, session, word, translation):
        new_word = Word(word=word, translation=translation)
        session.add(new_word)
        await session.commit()
        self.known_words.append({"word": word, "translation": translation})