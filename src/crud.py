from sqlalchemy.orm import Session
from models import User
#from pydantic import BaseModel

def get_user(db: Session, name: str, password: str):
    return db.query(User).filter(User.name == name, User.password == password ).first()

def create_user(db: Session, name: str, password: str):
    db_user = User(name=name, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
