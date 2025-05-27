from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./shortener.db"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()