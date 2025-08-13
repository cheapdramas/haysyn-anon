from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from backend.views import router as views_router
from backend.api import router as api_router

from backend.db.utils import db_helper 
from backend.config import STATIC_FILES_PATH
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
	db_helper.db_init()
	yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_FILES_PATH), name="static")
app.include_router(views_router)
app.include_router(api_router)



# if __name__ == "__main__":
# 	uvicorn.run(app = app, port = 8000,host="0.0.0.0")
