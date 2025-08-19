from pydantic import BaseModel, StringConstraints
from typing import Annotated 
from .post import MAX_TEXT_LEN 

class CommentBase(BaseModel):
    post_id: int

class CommentCreate(CommentBase):
    text: Annotated[str, StringConstraints(max_length=MAX_TEXT_LEN)]


class CommentRead(CommentCreate):
	id: int
