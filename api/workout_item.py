from typing import Optional

from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


router = APIRouter(prefix="/workout-item")

x = []
pk = 0


class WorkoutItem(BaseModel):
    pk: Optional[int]
    name: str
    iterations_count: int
    pause_before_item: int


@router.get("/", response_class=JSONResponse)
async def list(request: Request):
    return JSONResponse(content={"list": [item.dict() for item in x]})


@router.post("/", response_class=JSONResponse)
async def post(request: Request, workout_item: WorkoutItem):
    global pk
    pk = pk + 1
    workout_item.pk = pk
    x.append(workout_item)
    return JSONResponse(content={"status": "ok"})


@router.get("/{item_id}", response_class=JSONResponse)
async def get(request: Request, item_id: int):
    item = [i for i in x if i.pk == item_id]
    item = item[0].dict() if item else None
    return JSONResponse(content={"item": item})


@router.delete("/{item_id}", response_class=JSONResponse)
async def delete(request: Request, item_id: int):
    global x
    xx = [i for i in x if i.pk != item_id]
    x = xx
    return JSONResponse(content={"status": "ok"})


@router.post("/{item_id}", response_class=JSONResponse)
async def update(request: Request, item_id: int, workout_item: WorkoutItem):
    workout_item.pk = item_id
    global x
    xx = []
    for i in x:
        if i.pk != item_id:
            xx.append(i)
        else:
            xx.append(workout_item)
    x = xx
    return JSONResponse(content={"status": "ok"})
