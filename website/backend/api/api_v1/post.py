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
	PostCreate,
	PostLikeAction,
	PostRead,
    PostSortByOptions,
	PostsQuery
)
from backend.db.utils import db_helper
from backend.core.auth import id_generator, verify_token_depends
from backend.core.utils import fall_free
from backend.db.models import Post

import backend.core.Redis.scripts as redis_scripts



router = APIRouter()

@router.post("/post", response_model=PostRead)
@fall_free()
async def create_post(
    post_id: str,
	session: Annotated[
		AsyncSession,
		Depends(db_helper.session_getter)
	],
    token: str = Depends(verify_token_depends("bot"))
):
    """Creates post in database
    Takes post data from Redis by post_id
    Token must be released from bot
    """
    

    post_data: dict = await redis_scripts.remove_post(post_id) 
    created_post: Post  = await PostCrud.create_post(post_data, session)

    return created_post 

@router.get("/post",response_model=PostRead)
@fall_free()
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

@router.post("/posts",response_model=List[PostRead])
@fall_free()
async def get_posts_handler(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    post_query: PostsQuery
):
    """Returns <limit> of posts, starting from <offset>"""
    posts = await PostCrud.get_posts(session, post_query)

    return posts


@router.post("/submit_post")
@fall_free()
async def submit_post(
    post: PostCreate 
):
    """Puts post in Redis
    Redis then sends post_id to channel
    """
    post_id = str(next(id_generator))
    print("/submit_post telegram_user_id: ",post.telegram_user_id)
    await redis_scripts.add_post(post_id, post)
    return f"post key redis: 'post:{post_id}'"

@router.put("/like_post")
async def like_post(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    post_id: int,
    action: Annotated[str, PostLikeAction] = "plus"
):
    await PostCrud.like(session,post_id=post_id,action=action)
    likes = await PostCrud.get_likes(session,post_id=post_id)
    if likes == 5:
        await redis_scripts.publish_post_in_channel("to_tg_channel", post_id)
    return likes
            

@router.put("/dislike_post")
async def dislike_post(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    post_id: int,
    action: Annotated[str, PostLikeAction] = "plus"
):
    await PostCrud.dislike(session,post_id=post_id,action=action)
    return await PostCrud.get_dislikes(session,post_id=post_id)


@router.patch("/post_in_tg_channel")
async def in_tg_channel_handler(
     session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    post_id: int,
    set_to: bool,
    token: str = Depends(verify_token_depends("bot"))
):
    await PostCrud.in_tg_channel(session, post_id, set_to)
     

