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

from pydantic import Field

from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.crud import PostCrud 
from backend.schemas.post import (
	PostBase,
	PostRead,
    PostInRedis
)
from backend.db.utils import db_helper
from backend.core.auth import id_generator, verify_token_depends

import backend.core.Redis.scripts as redis_scripts



router = APIRouter()

#COMMENTED BECAUSE WE WILL PROBABLY ADD POSTS ONLY THROUGH WEBSOCKET CONNECTIONS WITH ADMIN FROM TELEGRAM BOT 
@router.post("/post", response_model=PostRead)
async def create_post(
    post_id: str,
	session: Annotated[
		AsyncSession,
		Depends(db_helper.session_getter)
	],
    token: str = Depends(verify_token_depends("bot"))
):
    post_data = await redis_scripts.remove_post(post_id) 
    post_model = await PostCrud.create_post(post_data, session)
    return post_model

@router.get("/post",response_model=PostRead)
async def get_post(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    id: int
):
    post = await PostCrud.get_post(id, session)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return post

@router.get("/posts",response_model=List[PostRead])
async def get_posts(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    start: Annotated[int,Field(gt=-1)],
    amount: Annotated[int,Field(gt=0, lt=101)]
):
    posts = await PostCrud.get_posts(
        start=start,
        amount=amount,
        session=session
    )
    return posts


@router.post("/submit_post")
async def submit_post(
    post: PostBase
):
    post_id = str(next(id_generator))
    await redis_scripts.add_post(post_id, post)
    return post_id 
 
