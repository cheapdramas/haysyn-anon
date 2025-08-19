from pydantic import BaseModel, StringConstraints
from typing import Annotated 
from dataclasses import dataclass

MAX_TITLE_LEN = 40
MAX_TEXT_LEN = 2200 

class PostBase(BaseModel):
	title: Annotated[str, StringConstraints(max_length=MAX_TITLE_LEN)]
	text: Annotated[str, StringConstraints(max_length=MAX_TEXT_LEN)]

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
	id: int
