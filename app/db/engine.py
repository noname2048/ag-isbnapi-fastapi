"""
sqlalchemy를 통해 db를 
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import dotenv_values
import os
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
config = dotenv_values(REPO_DIR / ".env")

dialect = "postgresql"
driver = "psycopg2"
username = config["DB_USER"]
password = config["DB_PASSWORD"]
host = "localhost"
port = "5432"
db_name = config["DB_NAME"]

SQLALCHEMY_DATABASE_URL = (
    f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
