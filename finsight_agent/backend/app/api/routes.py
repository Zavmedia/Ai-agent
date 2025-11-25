from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import auth, schemas
from ..db import models, database

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

from ..agents import orchestrator

@router.post("/agent")
async def run_agent(request: schemas.AgentRequest, current_user: models.User = Depends(auth.get_current_user)):
    graph = orchestrator.create_graph()
    inputs = {"query": request.query, "user_email": current_user.email}

    # The graph runs asynchronously. In a real app, you might use websockets
    # or a task queue to notify the user when the run is complete.
    # For this implementation, we'll run it synchronously and return the final state.
    final_state = {}
    for output in graph.stream(inputs):
        for key, value in output.items():
            final_state[key] = value

    return {"status": "success", "final_state": final_state}
