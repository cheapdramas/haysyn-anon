from pydantic import BaseModel, StringConstraints, Field
from typing import Annotated, Any
from dataclasses import dataclass
from enum import Enum


MAX_TITLE_LEN = 40
MAX_TEXT_LEN = 2200 

class PostBase(BaseModel):
	title: Annotated[str, StringConstraints(max_length=MAX_TITLE_LEN)]
	text: Annotated[str, StringConstraints(max_length=MAX_TEXT_LEN)]

class PostCreate(PostBase):
    telegram_user_id: str | None = None

class PostRead(PostCreate):
    id: int
    likes: int 
    dislikes: int

class PostInRedis(PostBase):
	id: str 

class PostSortByOptions(Enum):
    old="old"
    new="new"
    likes="likes"
    dislikes="dislikes"

class PostLikeAction(Enum):
    plus="plus"
    minus="minus"

class PostsQuery(BaseModel):
    offset: Annotated[int,Field(gt=-1)] = 0
    limit: Annotated[int,Field(gt=0, lt=101)] = 5
    sort_by: PostSortByOptions
    telegram_user_id: str | None = None
    exclude: list[int] | None = None
    in_tg_channel: bool | None = None 
