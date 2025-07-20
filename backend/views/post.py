from fastapi import APIRouter

router = APIRouter()

@router.get("/post/{id}")
async def post(id:int):
	return f"Wow {id}"