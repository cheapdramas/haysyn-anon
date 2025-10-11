from .models import Post, Comment 

from backend.schemas.post import (
	PostBase,
	PostCreate,
	PostRead
)
from backend.schemas.comment import (
	CommentBase,
	CommentCreate,
	CommentRead
)
from fastapi import HTTPException,status

from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

class PostCrud:
    @staticmethod
    async def create_post(
        post_create: PostCreate | dict,
        session: AsyncSession 
    ) -> Post:
        if isinstance(post_create, PostCreate):
            post = Post(**post_create.model_dump())
        else:
            post = Post(**post_create)

        try:
            session.add(post)
            await session.commit()
            await session.refresh(post)
            print("KINDA CREATING POST")
            return post
        except Exception as exc:
            await session.rollback()
            print("POST CREATE ERROR: ", exc)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) 

    @staticmethod
    async def get_post(
        id: int,
        session: AsyncSession
    ) -> Post | None:
        return await session.get(Post, id)
        
    @staticmethod
    async def get_posts(
        session: AsyncSession,
        amount: int,
        start: int = 0,
    ) -> Sequence[Post]:
        #select the latest <amount> of posts from <start> with limited text to 200 characters
        query = select(
            Post.id,
            Post.title,
            func.substr(Post.text, 1, 200).label("text")
        ).order_by(Post.id.desc()).offset(start).limit(amount)

        result = await session.execute(query)
        posts = result.all()
        return posts


class CommentCrud:
    @staticmethod
    async def create_comment(
        comment_create: CommentCreate,
        session: AsyncSession
    ) -> CommentRead:
        comment = Comment(**comment_create.model_dump())
        try:
            session.add(comment)
            await session.commit()
            await session.refresh(comment)
            return CommentRead.model_validate(comment) 
        except Exception as exc:
            await session.rollback()
            print("CREATE COMMENT ERROR: ", exc)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) 

    @staticmethod
    async def get_comments(
        session: AsyncSession,
        post_id: int,
        amount: int,
        start: int = 0,
    ) -> Sequence[Comment]:
        query = select(Comment).order_by(Comment.id.desc()).filter(Comment.post_id==post_id).offset(start).limit(amount)

        result = await session.execute(query)
        print(result)
        return result.scalars().all()
