from pydantic import BaseModel, StringConstraints
from typing import Annotated 
from dataclasses import dataclass
from enum import Enum

MAX_TITLE_LEN = 40
MAX_TEXT_LEN = 2200 

class PostBase(BaseModel):
	title: Annotated[str, StringConstraints(max_length=MAX_TITLE_LEN)]
	text: Annotated[str, StringConstraints(max_length=MAX_TEXT_LEN)]

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
	id: int

class PostInRedis(PostBase):
	id: str 


class PostModStatus(Enum):
    approved = "approved"
    declined = "declined"
class WSPostModerate(BaseModel):
    post_id: str
    status: PostModStatus
