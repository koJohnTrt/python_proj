from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import *

from db import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column("id", NUMERIC(8), primary_key=True)
    username = Column("username", VARCHAR(20), unique=True, nullable=False)
    password = Column("password", VARCHAR(20), nullable=False)

Base.metadata.create_all(bind=engine)