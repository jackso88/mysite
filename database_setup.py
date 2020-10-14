import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'Comment'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    subject = Column(String(250), nullable=False)
    message = Column(String(65535), nullable=False)


engine = create_engine('sqlite:///comments.db')

Base.metadata.create_all(engine)
