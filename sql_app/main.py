from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/workout-items/", response_model=schemas.WorkoutItem)
def create_workout_item(workout_item: schemas.WorkoutItemCreate, db: Session = Depends(get_db)):
    return crud.create_workout_item(db=db, workout_item=workout_item)


@app.get("/workout-items/", response_model=list[schemas.WorkoutItem])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workout_items = crud.get_workout_items(db, skip=skip, limit=limit)
    return workout_items
