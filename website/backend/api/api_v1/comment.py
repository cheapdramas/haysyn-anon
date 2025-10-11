from fastapi import APIRouter, Depends
from typing import Annotated, List

from backend.db.crud import CommentCrud
from backend.schemas.comment import CommentCreate,CommentRead
from backend.db.utils import db_helper

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/comment",response_model=CommentRead)
async def create_comment(
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter)
    ],
    comment: CommentCreate,
):
    return await CommentCrud.create_comment(comment, session)


@router.get("/comments",response_model=List[CommentRead])
async def get_comments(
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter)
    ],
    post_id: int,
    amount: int,
    start: int = 0,
):
    comments = await CommentCrud.get_comments(
        session=session,
        post_id=post_id,
        amount=amount,
        start=start
    )
    print(comments)
    return comments
