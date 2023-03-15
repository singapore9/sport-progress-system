from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def get_workout_item(db: Session, workout_item_id: int):
    return db.query(models.WorkoutItem).filter(models.WorkoutItem == workout_item_id).first()


def get_workout_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WorkoutItem).offset(skip).limit(limit).all()


def get_workout_items_by_user_id(db: Session, user_id: str, skip: int=0, limit: int=100):
    return db.query(models.WorkoutItem).filter(models.WorkoutItem.user_id == user_id).offset(skip).limit(limit).all()


def create_workout_item(db: Session, workout_item: schemas.WorkoutItemCreate):
    id = int(datetime.utcnow().timestamp())
    db_workout_item = models.WorkoutItem(**workout_item.dict(), pk=id)
    db.add(db_workout_item)
    db.commit()
    db.refresh(db_workout_item)
    return db_workout_item
