from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config.config import get_config

router = APIRouter(
    prefix='',
    tags=['welcome']
)

templates = Jinja2Templates(directory=get_config().TEMPLATE_DIR)

@router.get('/', response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse(
        request=request, name='welcome.html', context={}
    )