from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    word = Column(String, index=True)
    translation = Column(String)

class UserProgress(Base):
    __tablename__ = 'user_progress'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    word = Column(String, index=True)
    learned = Column(Boolean, default=False)

class Text(Base):
    __tablename__ = 'texts'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)