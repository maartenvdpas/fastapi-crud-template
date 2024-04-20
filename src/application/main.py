import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.config import get_config
from routes.welcome import router as WelcomeRouter
from routes.api.index import router as APIRouter

app = FastAPI()
app.mount('/templates', StaticFiles(directory=get_config().TEMPLATE_DIR), name='templates')
app.mount('/static', StaticFiles(directory=get_config().STATIC_DIR), name='static')
app.include_router(WelcomeRouter)
app.include_router(APIRouter)

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)