from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

BASE_DIR=os.path.dirname(os.path.realpath(__file__))
DB_URL = 'sqlite:///'+BASE_DIR+'/test.db'
print(DB_URL)
engine = create_engine(DB_URL, connect_args={'check_same_thread': False})

# from dotenv import load_dotenv
# load_dotenv()
# password = os.getenv('PASSWORD')
# db_id = os.getenv('DBID')
# conn_str = f"postgresql://postgres.{db_id}:{password}@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"
# print(conn_str)
# engine=create_engine(conn_str,echo=True)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()