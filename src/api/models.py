from sqlalchemy import Column, Float, Integer, String
from database import Base, engine

# define Location model for storing cities
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

# create database table
Base.metadata.create_all(bind=engine)
