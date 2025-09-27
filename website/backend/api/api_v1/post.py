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
	PostRead,
    PostInRedis
)
from backend.db.utils import db_helper
from backend.core.auth import create_jwt, verify_token_depends, id_generator
from backend.core.websockets_control import ws_connections, send_to_admins
import backend.core.Redis.scripts as redis_scripts



router = APIRouter()

#COMMENTED BECAUSE WE WILL PROBABLY ADD POSTS ONLY THROUGH WEBSOCKET CONNECTIONS WITH ADMIN FROM TELEGRAM BOT 
# @router.post("/post", response_model=PostRead)
# async def create_post(
# 	post_create: PostCreate,
# 	session: Annotated[
# 		Session,
# 		Depends(db_helper.session_getter)
# 	],
#     token: str = Depends(verify_token_depends("bot"))
# ):
# 	post_model = PostCrud.create_post(post_create, session)
# 	return post_model

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



@router.post("/submit_post")
async def submit_post(post: PostBase):
    post_id = str(next(id_generator))

    await send_to_admins([PostInRedis(id=post_id,**post.model_dump())])

    seen_by=list(ws_connections.keys())
    await redis_scripts.add_post(post_id, post, seen_by)

    print(ws_connections)

    return post_id 
    


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
