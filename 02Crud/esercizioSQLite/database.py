from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace 'username', 'password', 'hostname', 'port', and 'database_name' PostgreSQL
#DATABASE_URL = "postgresql://username:password@hostname:port/database_name"

DATABASE_URL="sqlite:///todo.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Create the SessionLocal
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)