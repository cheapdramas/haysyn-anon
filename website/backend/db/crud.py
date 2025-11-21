from .models import Post, Comment 

from backend.schemas.post import (
	PostBase,
	PostCreate,
	PostLikeAction,
	PostRead,
    PostSortByOptions
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
from sqlalchemy import func, update, case

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
        sort_by: str,
        amount: int,
        start: int = 0,
    ) -> Sequence[PostRead]:
        query = select(
            Post.id,
            Post.title,
            Post.likes,
            Post.dislikes,
            func.substr(Post.text, 1, 200).label("text")
        )

        if sort_by == "old":
            query = query.offset(start).limit(amount)

        if sort_by == "new":
            query = query.order_by(Post.id.desc()).offset(start).limit(amount)

        if sort_by == "likes":
            order_expr = case(
                (Post.likes == 0, 0),   
                else_=1                
            ).desc()

            query = query.order_by(
                order_expr,
                Post.likes.desc(),
                Post.id.desc()
            ).offset(start).limit(amount)

        if sort_by == "dislikes":
            order_expr = case(
                (Post.dislikes== 0, 0),   
                else_=1                
            ).desc()

            query = query.order_by(
                order_expr,
                Post.dislikes.desc(),
                Post.id.desc()
            ).offset(start).limit(amount)


        result = await session.execute(query)
        posts = result.all()
        return posts

    @staticmethod
    async def get_likes(
        session: AsyncSession,
        post_id: int
    ):
        try:
            q = select(Post.likes).where(Post.id==post_id) 
            res = await session.execute(q)
            return res.scalar_one()
        except Exception as e:
            print("Error occured in post get like method: ", str(e))

    @staticmethod
    async def get_dislikes(
        session: AsyncSession,
        post_id: int
    ):
        try:
            q = select(Post.dislikes).where(Post.id==post_id) 
            res = await session.execute(q)
            return res.scalar_one()
        except Exception as e:
            print("Error occured in post get like method: ", str(e))


    @staticmethod
    async def like(
        session: AsyncSession,
        post_id: int,
        action: PostLikeAction
    ):
        add = 1
        if action == "minus":
            add = - 1

        try:
            q = update(Post).where(Post.id==post_id).values(likes=Post.likes  + add)
            await session.execute(q)
            await session.commit()

        except Exception as e:
            print("Error occured in post like method: ",str(e))

    @staticmethod
    async def dislike(
        session: AsyncSession,
        post_id: int,
        action: PostLikeAction
    ):
        add = 1
        if action == "minus":
            add = - 1

        try:
            q = update(Post).where(Post.id==post_id).values(dislikes=Post.dislikes + add)
            await session.execute(q)
            await session.commit()
        except Exception as e:
            print("Error occured in post dislike method: ",str(e))


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
