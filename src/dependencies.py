from sqlalchemy.orm import Session
from database import SessionLocal

# Dependency to get the DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
