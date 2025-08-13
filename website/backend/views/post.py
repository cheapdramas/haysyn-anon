from fastapi import APIRouter, Request

from backend.utils.templates import templates
router = APIRouter()

@router.get("/post/{id}")
async def post(request: Request):
	return templates.TemplateResponse("post.html", {
		"request": request,
		"is_homepage": False 
	})
