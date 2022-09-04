from fastapi import Request, Form, APIRouter
from fastapi.responses import JSONResponse
from firebase_admin import db

from firebase import (
    default_app, BASE_PATH, EXERCISES_PATH, EXERCISES_NEXT_ID_PATH, EXERCISES_NEXT_ID_KEY, EXERCISES_TRANSLATION_KEY
)


router = APIRouter(prefix="/exercise")


@router.get("/", response_class=JSONResponse)
async def list(request: Request):
    ref = db.reference(EXERCISES_PATH, default_app)
    result: dict = ref.get()
    return JSONResponse(content={"list": [sorted(result.values())]})


@router.post("/", response_class=JSONResponse)
async def post(request: Request, name: str = Form(...)):
    ref = db.reference(EXERCISES_NEXT_ID_PATH, default_app)
    nextid: int = ref.get()
    item = {f"id{nextid}": name}

    ref = db.reference(BASE_PATH, default_app)
    ref.update({EXERCISES_NEXT_ID_KEY: nextid + 1})

    ref = db.reference(EXERCISES_PATH, default_app)
    items: dict = ref.get()
    items.update(item)
    ref.update(items)
    return JSONResponse(content={"status": "ok"})


@router.get("/translate/{language}", response_class=JSONResponse)
async def translated_list(request: Request, language: str):
    ref = db.reference(EXERCISES_PATH, default_app)
    exercises_result: dict = ref.get()

    ref = db.reference(EXERCISES_TRANSLATION_KEY, default_app)
    translations_result: dict = ref.get()
    translations = {}
    for inner_key, exercise_name in exercises_result.items():
        translation = translations_result.get(inner_key, {}).get(language, exercise_name)
        translations[exercise_name] = translation
    return JSONResponse(content={"list": [sorted(translations.items(), key=lambda x: x[0])]})
