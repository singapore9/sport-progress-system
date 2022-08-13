from typing import Optional

from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from firebase_admin import db

from firebase import (
    default_app, BASE_PATH, WORKOUT_ITEMS_PATH, WORKOUT_ITEMS_NEXT_ID_PATH, WORKOUT_ITEMS_KEY, WORKOUT_ITEMS_NEXT_ID_KEY
)


router = APIRouter(prefix="/workout-item")


class WorkoutItem(BaseModel):
    pk: Optional[int]
    name: str
    iterations_count: int
    pause_before_item: int
    timestamp: int
    user_id: str


@router.get("/", response_class=JSONResponse)
async def list(request: Request):
    ref = db.reference(WORKOUT_ITEMS_PATH, default_app)
    result: dict = ref.get()
    return JSONResponse(content={"list": [item for item in sorted(result.values(), key=lambda x: x['pk'])]})


@router.post("/", response_class=JSONResponse)
async def post(request: Request, workout_item: WorkoutItem):
    ref = db.reference(WORKOUT_ITEMS_NEXT_ID_PATH, default_app)
    nextid: int = ref.get()
    workout_item.pk = nextid
    item = {f"id{nextid}": workout_item.dict()}

    ref = db.reference(BASE_PATH, default_app)
    ref.update({WORKOUT_ITEMS_NEXT_ID_KEY: nextid + 1})

    ref = db.reference(WORKOUT_ITEMS_PATH, default_app)
    items: dict = ref.get()
    items.update(item)
    ref.update(items)
    return JSONResponse(content={"status": "ok"})


@router.get("/{item_id}", response_class=JSONResponse)
async def get(request: Request, item_id: int):
    ref = db.reference(WORKOUT_ITEMS_PATH, default_app)
    items: dict = ref.get()

    result_item = None
    for _id, item in items.items():
        if item['pk'] == item_id:
            result_item = item
            break
    return JSONResponse(content={"item": result_item})


@router.delete("/{item_id}", response_class=JSONResponse)
async def delete(request: Request, item_id: int):
    ref = db.reference(WORKOUT_ITEMS_PATH, default_app)
    items: dict = ref.get()

    updated_items = {key: item for key, item in items.items() if item['pk'] != item_id}
    ref = db.reference(BASE_PATH, default_app)
    ref.update({WORKOUT_ITEMS_KEY: updated_items})
    return JSONResponse(content={"status": "ok"})


@router.post("/{item_id}", response_class=JSONResponse)
async def update(request: Request, item_id: int, workout_item: WorkoutItem):
    ref = db.reference(WORKOUT_ITEMS_PATH, default_app)
    items: dict = ref.get()

    updated_items = {}
    for _id, item in items.items():
        if item['pk'] != item_id:
            updated_items[_id] = item
        else:
            workout_item.pk = item_id
            updated_items[_id] = workout_item.dict()
    ref.update(updated_items)
    return JSONResponse(content={"status": "ok"})
