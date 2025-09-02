import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use Railway-provided environment variables
DB_USER = os.getenv("mysqluser")
DB_PASSWORD = os.getenv("mysqlpassword")
DB_HOST = os.getenv("mysqlhost")
DB_PORT = os.getenv("mysqlport", "3306")
DB_NAME = os.getenv("mysqldatabase")

# Build connection string
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base for models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()