from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from api.root import router as api_router
from constants import ALLOWED_HOSTS

origins = []
origins.extend(ALLOWED_HOSTS)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

templates = Jinja2Templates(directory="templates/")

favicon_path = 'templates/logo.png'


@app.get('/logo.png', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('base.html', context={'request': request})
