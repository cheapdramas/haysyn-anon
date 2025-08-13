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

from backend.db.crud import PostCrud 

from backend.schemas.post import (
	PostBase,
	PostCreate,
	PostRead
) 

from backend.db.utils import db_helper

router = APIRouter()

@router.post("/post", response_model=PostRead)
async def create_post(
	post_create: PostCreate,
	session: Annotated[
		Session,
		Depends(db_helper.session_getter)
	]
):
	post_model = PostCrud.create_post(post_create, session)
	return post_model

@router.get("/post",response_model=PostRead)
async def get_post(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter)
    ],
    id: int
):
    post = PostCrud.get_post(id, session)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return post

@router.get("/posts",response_model=List[PostRead])
async def get_posts(
	session: Annotated[
		Session,
		Depends(db_helper.session_getter)
	],
	start: Optional[int] = 0,
	amount: Optional[int] = None
):
	if amount is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
	posts = PostCrud.get_posts(
		start=start,
		amount=amount,
		session=session
	)
	return posts
