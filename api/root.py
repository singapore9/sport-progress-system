from fastapi import APIRouter
from api.exercise import router as exercise_router
from api.workout_item import router as workout_item_router


router = APIRouter(prefix="/api")
router.include_router(exercise_router)
router.include_router(workout_item_router)
