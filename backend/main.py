from fastapi import FastAPI
from contextlib import contextmanager
from views import router as views_router
from api import router as api_router

from db.utils import db_helper 
import uvicorn

@contextmanager
def lifespan():
	db_helper.db_init()
	yield

app = FastAPI()
app.include_router(views_router)
app.include_router(api_router)


if __name__ == "__main__":
	uvicorn.run(app = app, port = 8000,host="0.0.0.0")
