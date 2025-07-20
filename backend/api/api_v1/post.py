from fastapi import (
	APIRouter,
	Depends,
	status
)

from fastapi.exceptions import HTTPException

from typing import (
	Annotated,
	Optional,
	List
)
from sqlalchemy.orm import Session

from db import crud

from schemas.post import (
	PostBase,
	PostCreate,
	PostRead
) 

from db.utils import db_helper

router = APIRouter()

@router.post("", response_model=PostRead)
async def create_post(
	post_create: PostCreate,
	session: Annotated[
		Session,
		Depends(db_helper.session_getter)
	]
):
	post_model = crud.create_post(post_create, session)
	return post_model

@router.get("",response_model=PostRead | List[PostRead])
async def get_post(
	session: Annotated[
		Session,
		Depends(db_helper.session_getter)
	],
	id: Optional[int] = None,
	start: Optional[int] = 0,
	amount: Optional[int] = None
):
	if id is not None:
		#return post requested by {id}
		post = crud.get_post(id, session)
		print(post)
		if post == None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
		return post
	
	#return {amont} posts from start 
	if amount is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
	posts = crud.get_posts(
		start=start,
		amount=amount,
		session=session
	)
	return posts


	