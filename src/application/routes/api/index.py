from fastapi import APIRouter

router = APIRouter(
    prefix='/api',
    tags=['api']
)

@router.get(path='/', status_code=200)
async def index():
    return {'status': 200, 'msg': 'Hello World!'}