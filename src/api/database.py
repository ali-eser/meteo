from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

# load database credentials from environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# set up PostgreSQL database connection
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

# create SQLAlchemy base class
class Base(DeclarativeBase):
    pass

# create and close a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
