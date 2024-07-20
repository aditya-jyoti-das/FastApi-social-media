from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

import os

from .config import settings


MYSQL_HOST=settings.database_hostname
MYSQL_USER=settings.database_username
MYSQL_PASSWORD=settings.database_password
MYSQL_DB=settings.database_name
MYSQL_PORT=settings.database_port

engine = create_engine(f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
                            pool_recycle=3600, echo=True)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
