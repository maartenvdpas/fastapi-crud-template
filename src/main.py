import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from application.pages.welcome import router as WelcomeRouter
from application.api.index import router as APIRouter

app = FastAPI()
app.mount('/pages', StaticFiles(directory='src/application/pages/templates'), name='pages')
app.include_router(WelcomeRouter)
app.include_router(APIRouter)

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)