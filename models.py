from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  
    word = Column(String(length=255), nullable=False)
    translation = Column(String(length=255), nullable=False)

    def __repr__(self):
        return f"<Word(id={self.id}, user_id={self.user_id}, word='{self.word}', translation='{self.translation}')>"

class Text(Base):
    __tablename__ = 'texts'  

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Text(id={self.id}, content='{self.content[:20]}...')>"