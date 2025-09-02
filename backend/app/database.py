import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use Railway-injected environment variables
DB_USER = os.getenv("mysqluser")
DB_PASSWORD = os.getenv("mysqlpassword")
DB_HOST = os.getenv("mysqlhost")
DB_PORT = os.getenv("mysqlport", "3306")
DB_NAME = os.getenv("mysqldatabase")

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
