from pydantic import BaseModel, StringConstraints
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

