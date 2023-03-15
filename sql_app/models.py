from sqlalchemy import Column, Integer, String

from .database import Base


class WorkoutItem(Base):
    __tablename__ = "workout_items"

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    iterations_count = Column(Integer)
    pause_before_item = Column(Integer)
    timestamp = Column(Integer)
    user_id = Column(String)
