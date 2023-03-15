from typing import Optional

from pydantic import BaseModel


class WorkoutItemBase(BaseModel):
    pk: Optional[int]
    name: str
    iterations_count: int
    pause_before_item: int
    timestamp: int
    user_id: str


class WorkoutItemCreate(WorkoutItemBase):
    pass


class WorkoutItem(WorkoutItemBase):
    class Config:
        orm_mode = True
