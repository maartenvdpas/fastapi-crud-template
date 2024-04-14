from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='',
    tags=['welcome']
)

templates = Jinja2Templates(directory='src/application/pages/templates')

@router.get('/', response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse(
        request=request, name='welcome.html', context={}
    )