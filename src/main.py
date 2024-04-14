import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from application.pages.welcome import router as WelcomeRouter

app = FastAPI()
app.mount('/pages', StaticFiles(directory='src/application/templates'), name='pages')
app.include_router(WelcomeRouter)

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)