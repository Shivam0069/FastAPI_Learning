from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# load_dotenv()
# SQLITE3
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# env_path = os.path.join(os.path.dirname(__file__), ".env")
# load_dotenv(dotenv_path=env_path)

# Check if the file is loading


# SQLALCHEMY_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL")

# POSTGRESQL DATABASE

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
