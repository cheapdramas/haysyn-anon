from fastapi import APIRouter, Request
from backend.utils.templates import templates

router = APIRouter()

@router.get("/contacts")
async def contacts(request: Request):
	return templates.TemplateResponse("contacts.html", {
		"request": request,
		"is_homepage": False 
	})
