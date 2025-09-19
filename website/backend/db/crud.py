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

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

class PostCrud:
    @staticmethod
    def create_post(
        post_create: PostCreate,
        session: Session 
    ) -> Post:
        post = Post(**post_create.model_dump())
        try:
            session.add(post)
            session.commit()
            return post
        except Exception as exc:
            session.rollback()
            print("POST CREATE ERROR: ", exc)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) 

    @staticmethod
    def get_post(
        id: int,
        session: Session
    ) -> PostRead:
        return session.get(Post, id)
        
    @staticmethod
    def get_posts(
        session: Session,
        amount: int,
        start: int = 0,
    ) -> List[PostRead]:
        return session.query(Post).order_by(Post.id.desc()).offset(start).limit(amount).all()


class CommentCrud:
    @staticmethod
    def create_comment(
        comment_create: CommentCreate,
        session: Session
    ) -> Comment:
        comment = Comment(**comment_create.model_dump())
        try:
            session.add(comment)
            session.commit()
            return comment
        except Exception as exc:
            session.rollback()
            print("CREATE COMMENT ERROR: ", exc)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) 

    @staticmethod
    def get_comments(
        session: Session,
        post_id: int,
        amount: int,
        start: int = 0,
    ) -> List[Comment]:
        return session.query(Comment).order_by(Comment.id.desc()).filter(Comment.post_id==post_id).offset(start).limit(amount)
