from sqlalchemy import Column, Integer, String
from database import Base

class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    word = Column(String, index=True)
    translation = Column(String)