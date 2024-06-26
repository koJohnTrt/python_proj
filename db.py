from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environs import Env

env = Env()
env.read_env()

DATABASE = env("DATABASE")
DB_HOST  = env("DB_HOST")
DB_PORT  = env("DB_PORT")
DB_NAME  = env("DB_NAME")
DB_USER  = env("DB_USER")
DB_PASS  = env("DB_PASS")

SQLALCHEMY_DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(DATABASE, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Base = declarative_base()

