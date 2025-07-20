# Landing page <3

from fastapi import APIRouter, Request
from utils.templates import templates
router = APIRouter()

@router.get("/",name="home")
async def index(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="index.html"
	) 