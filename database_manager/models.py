from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Integer, JSON

Base = declarative_base()

class Listing(Base):
    __tablename__ = 'hotels'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    room_type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    images = Column(JSON, nullable=False)
