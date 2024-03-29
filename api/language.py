from fastapi import Form, Request, APIRouter
from fastapi.responses import JSONResponse
from firebase_admin import db

from firebase import (
    default_app, LANGUAGE_ITEMS_PATH
)


router = APIRouter(prefix="/language")


@router.get("/{user_id}", response_class=JSONResponse)
async def get(request: Request, user_id: str):
    ref = db.reference(LANGUAGE_ITEMS_PATH, default_app)
    items: dict = ref.get()
    lang = items.get(user_id, None)

    if user_id not in items:
        items[user_id] = lang
        ref.update(items)
    return JSONResponse(content={"language": lang})


@router.post("/{user_id}", response_class=JSONResponse)
async def post(request: Request, user_id: str, language: str = Form(...)):
    ref = db.reference(LANGUAGE_ITEMS_PATH, default_app)
    items: dict = ref.get()
    items[user_id] = language
    ref.update(items)
    return JSONResponse(content={"status": "ok"})
