from sqlalchemy.orm import Session
from . import models, schemas
from .. import auth

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_strategy(db: Session, strategy: schemas.StrategyCreate, user_id: int):
    db_strategy = models.Strategy(**strategy.dict(), owner_id=user_id)
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

def get_strategies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Strategy).offset(skip).limit(limit).all()
