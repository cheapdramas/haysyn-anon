from pydantic import BaseModel, StringConstraints
from typing import Annotated 
from .post import PostConfig

class CommentBase(BaseModel):
    post_id: int

class CommentCreate(CommentBase):
    text: Annotated[str, StringConstraints(max_length=PostConfig.max_text_len)]


class CommentRead(CommentCreate):
	id: int
