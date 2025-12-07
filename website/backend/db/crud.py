from .models import Post, Comment 

from backend.schemas.post import (
	PostBase,
	PostCreate,
	PostLikeAction,
	PostRead,
    PostSortByOptions,
	PostsQuery
)
from backend.schemas.comment import (
	CommentBase,
	CommentCreate,
	CommentRead
)
from fastapi import HTTPException,status

from typing import Sequence
from sqlalchemy.orm import Session, query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import except_, func, update, case

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
    async def get_posts_tg_user_id(
        telegram_user_id: str,
        session: AsyncSession
    ) -> Sequence[Post]:
        query = select(Post).filter(Post.telegram_user_id==telegram_user_id)
        result = await session.execute(query)
        posts = result.scalars().all()
        return posts

        
    @staticmethod
    async def get_posts(
        session: AsyncSession,
        post_query: PostsQuery 
    ) -> Sequence[PostRead]:
        query = select(
            Post.id,
            Post.title,
            Post.in_tg_channel,
            Post.likes,
            Post.dislikes,
            func.substr(Post.text, 1, 200).label("text")
        )
        sort_by = post_query.sort_by.value
        if post_query.in_tg_channel != None:
            query = query.where(Post.in_tg_channel==post_query.in_tg_channel)

            

        if post_query.exclude:
            query = query.where(Post.id.notin_(post_query.exclude))

        if post_query.telegram_user_id:
            query = query.where(Post.telegram_user_id == post_query.telegram_user_id)

        if sort_by == "old":
            query = query.order_by(Post.id.asc())

        elif sort_by == "new":
            query = query.order_by(Post.id.desc())

        elif sort_by == "likes":
            order_expr = case(
                (Post.likes == 0, 0),
                else_=1
            ).desc()

            query = query.order_by(
                order_expr,
                Post.likes.desc(),
                Post.id.desc()
            )

        elif sort_by == "dislikes":
            order_expr = case(
                (Post.dislikes == 0, 0),
                else_=1
            ).desc()

            query = query.order_by(
                order_expr,
                Post.dislikes.desc(),
                Post.id.desc()
            )

        # 🔥 LIMIT + OFFSET (спільно для всіх)
        query = query.offset(post_query.offset).limit(post_query.limit)

        # 🔥 Виконання
        result = await session.execute(query)
        return result.all()

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
            print("Error occured in post dislike method: ", str(e))

    @staticmethod 
    async def in_tg_channel(
        session: AsyncSession,
        post_id: int,
        set_to: bool = True,
    ):
        try:
            q = update(Post).where(Post.id==post_id).values(in_tg_channel=set_to)
            await session.execute(q)
            await session.commit()
        except Exception as e:
            print("Error occured in in_tg_channel method: ", str(e))



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
