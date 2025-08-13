# Landing page <3

from fastapi import APIRouter, Request
from backend.utils.templates import templates
router = APIRouter()

@router.get("/",name="home")
async def index(request: Request):
	return templates.TemplateResponse("index.html", {
		"request": request,
		"is_homepage": True
	})
