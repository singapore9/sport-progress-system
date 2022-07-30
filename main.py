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

ALLOWED_STATIC_FILES = [
    'logo.png',
    'chartBuilder.js'
]


@app.get('/static/{filepath}', include_in_schema=False)
async def get_file(filepath: str):
    if filepath in ALLOWED_STATIC_FILES:
        return FileResponse(f'templates/{filepath}')
    return None


@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('base.html', context={'request': request})
