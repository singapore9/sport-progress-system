from fastapi import Request, Form, APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/exercise")

x = []


@router.get("/", response_class=JSONResponse)
async def list(request: Request):
    return JSONResponse(content={"list": x})


@router.post("/", response_class=JSONResponse)
async def post(request: Request, name: str = Form(...)):
    x.append(name)
    return JSONResponse(content={"status": "ok"})
