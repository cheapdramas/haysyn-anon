from .models import Post 
from schemas.post import (
	PostBase,
	PostCreate,
	PostRead
)

from typing import List
from sqlalchemy.orm import Session


def create_post(
	post_create: PostCreate,
	session: Session 
) -> Post:
	post = Post(**post_create.model_dump())
	session.add(post)
	session.commit()
	return post

def get_post(
	id: int,
	session: Session
) -> PostRead:
	return session.get(Post, id)
	

def get_posts(
	session: Session,
	start: int = 0,
	amount: int = None, 
) -> List[PostRead]:
	return session.query(Post).order_by(Post.id.desc()).offset(start).limit(amount).all()
