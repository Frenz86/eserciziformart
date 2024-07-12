from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

####################################################################################
#postgresql://postgres.loxlelduixpehvvapdvb:[YOUR-PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:5432/postgres
import os
from dotenv import load_dotenv
load_dotenv()

password = os.environ.get('PASSWORD')
db_id = os.environ.get('DBID')
dialect = "postgresql"
username = "postgres"
host = "aws-0-eu-central-1.pooler.supabase.com"
port = 5432
database = "postgres"

DATABASE_URL = f"{dialect}://{username}.{db_id}:{password}@{host}:{port}/{database}"

#DATABASE_URL="sqlite:///todo.db"

####################################################################################
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Create the SessionLocal
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)