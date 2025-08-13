from operator import pos
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

from backend.db.models import Comment
from backend.db.crud import CommentCrud

from backend.schemas.comment import (
    CommentBase,
    CommentCreate,
    CommentRead
)

from backend.db.utils import db_helper

router = APIRouter()

@router.post("/comment", response_model=CommentRead)
async def create_comment(
    comment: CommentCreate,
    session: Annotated[
        Session,
        Depends(db_helper.session_getter)
    ]
):
    comment_model = CommentCrud.create_comment(comment, session)
    return comment_model

@router.get("/comments", response_model=List[CommentRead])
async def get_comments(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter)
    ],
    post_id: int,
    amount: int,
    start: int = 0,
):
    comments = CommentCrud.get_comments(
        session=session,
        post_id=post_id,
        amount=amount,
        start=start
    )
    return comments
