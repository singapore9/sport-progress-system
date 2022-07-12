from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from api.root import router as api_router

app = FastAPI()
app.include_router(api_router)

templates = Jinja2Templates(directory="templates/")

favicon_path = 'templates/logo.png'


@app.get('/logo.png', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('base.html', context={'request': request})