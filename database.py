#database.py 

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the PostgreSQL connection string from environment variables
# Format: postgresql://username:password@host:port/database
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine - this manages the connection pool
engine = create_engine(DATABASE_URL)

# Create a session factory - sessions handle database transactions
# autocommit=False: We control when to commit changes
# autoflush=False: We control when to flush changes to database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all our database models
Base = declarative_base()

# Dependency function to get database session
# Used by FastAPI to inject database connection into endpoints
def get_db():
    db = SessionLocal()  # Create new session
    try:
        yield db  # Provide session to the endpoint
    finally:
        db.close()  # Always close session when done