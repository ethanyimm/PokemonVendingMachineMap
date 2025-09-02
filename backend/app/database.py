import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use Railway-injected environment variables (uppercase!)
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_HOST = os.getenv("MYSQLHOST")
DB_PORT = os.getenv("MYSQLPORT", "3306")
DB_NAME = os.getenv("MYSQLDATABASE")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()