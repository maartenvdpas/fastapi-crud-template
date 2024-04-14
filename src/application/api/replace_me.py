from fastapi import APIRouter

router = APIRouter(
    prefix='/api',
    tags=['api']
)

@router.get(path='/', status_code=200)
async def test():
    return {'status': 200, 'msg': 'Hello World!'}